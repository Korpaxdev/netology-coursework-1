import re
from datetime import datetime
from requests import get
from utils.helpers import print_success


class Vk:
    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token: str):
        self.__token = token
        self.__base_params = {'access_token': self.__token, 'v': '5.131'}
        self.photos = []
        self.__count_names = 1

    def __set_name(self, like_count: int, ext: str) -> str:
        now_date = datetime.now().strftime('%d-%m-%Y')
        template_names = {'default': f"{like_count}.{ext}", 'date': f"{like_count}_{now_date}.{ext}",
                          'count': f"{like_count}_{now_date}({self.__count_names}).{ext}"}
        name = template_names['default']
        for photo in self.photos:
            if photo['file_name'] == template_names['default']:
                name = template_names['date']
            if photo['file_name'] == template_names['date']:
                name = template_names['count']
                self.__count_names += 1
        return name

    @staticmethod
    def __get_larger_image(sizes: list) -> tuple:
        size_types = ('w', 'z', 'y', 'x', 'm', 's')
        for s_type in size_types:
            image_list = list(filter(lambda p: p['type'] == s_type, sizes))
            if image_list:
                large_image = image_list[0]
                return large_image['url'], large_image['type']

    @staticmethod
    def __get_extension_from_url(url: str) -> str:
        match = re.search(r"(?i)(?P<ext>jpg|png|webp)", url)
        if match:
            return match.groupdict()['ext']
        return 'jpg'

    def __set_max_size_photos(self, data: dict) -> None:
        items = data['response']['items']
        print_success(f'Получено {len(items)} фотографий')
        for i in items:
            count_likes = i['likes']['count']
            url, size = self.__get_larger_image(i['sizes'])
            name = self.__set_name(count_likes, self.__get_extension_from_url(url))
            photo = {'file_name': name, 'file_url': url, 'size': size}
            self.photos.append(photo)

    def get_photos(self, owner_id: int | None = None, count: int = 5) -> list:
        url = self.BASE_URL + 'photos.get'
        params = {'album_id': 'profile', 'owner_id': owner_id, 'count': count, 'extended': 1, 'photo_sizes': 1,
                  'rev': 1}
        params.update(self.__base_params)
        response = get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('error', None):
            raise Exception(data['error']['error_msg'])
        if data.get('response', None):
            self.__set_max_size_photos(data)
        return self.photos
