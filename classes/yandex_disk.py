import json
from progress.bar import IncrementalBar
from requests import get, post, put
from utils.helpers import print_success


class YandexDisk:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.__token = token
        self.__base_headers = {'Authorization': token}

    def __check_folder(self, folder: str):
        params = {'path': folder}
        response = get(self.BASE_URL, params=params, headers=self.__base_headers)
        if response.status_code not in [200, 404]:
            response.raise_for_status()
        return response.status_code == 200

    def __create_folder(self, folder: str) -> bool:
        params = {'path': folder}
        response = put(self.BASE_URL, params=params, headers=self.__base_headers)
        response.raise_for_status()
        return True

    @staticmethod
    def __create_log_file(files_list: list):
        write_data = [{'file_name': f['file_name'], 'size': f['size']} for f in files_list]
        with open('../log.json', 'w+', encoding='utf-8') as f:
            json.dump(write_data, f, indent=4)
        print_success('Файл log.json создан')

    def upload_files(self, files_list: list, folder: str | None = None):
        bar = IncrementalBar('Загружаем фотографии на Яндекс Диск', max=len(files_list))
        url = self.BASE_URL + '/upload'
        if folder and not self.__check_folder(folder):
            self.__create_folder(folder)
        for f in files_list:
            file_path = f"{folder}/{f['file_name']}" if folder else f['file_name']
            params = {'path': file_path, 'url': f['file_url']}
            response = post(url, params=params, headers=self.__base_headers)
            response.raise_for_status()
            bar.next()
        bar.finish()
        print_success('Фотографии загружены')
        self.__create_log_file(files_list)
