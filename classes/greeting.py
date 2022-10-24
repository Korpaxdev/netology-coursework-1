from re import match
from utils.helpers import print_error, color_input, print_title
from utils.messages_variables import messages, error_messages


class Greeting:
    @staticmethod
    def __get_token(message: str, error_message=error_messages['required']):
        while True:
            token = color_input(message)
            if not token:
                print_error(error_message)
                continue
            return token

    @staticmethod
    def __get_number_value(default: int | None, message: str,
                           error_message: str = error_messages['number']) -> int | None:
        while True:
            value = color_input(message)
            if not value:
                return default
            if value and not value.isdigit():
                print_error(error_message)
                continue
            return int(value)

    @staticmethod
    def __get_folder_name(default: int | str, message: str,
                          error_message: str = error_messages['folder_name']) -> int | str:
        while True:
            folder_name = color_input(message)
            if not folder_name:
                return default
            if match(r"[\\/:*?\"<>|]+", folder_name):
                print_error(error_message)
                continue
            return folder_name

    def __init__(self):
        print_title(messages['greeting'])
        print_title(messages['info'])
        self.__vk_token = self.__get_token(messages['vk_token'])
        self.__yandex_token = self.__get_token(messages['yandex_token'])
        self.vk_user_id = self.__get_number_value(None, messages['vk_user_id'])
        self.photos_count = self.__get_number_value(5, messages['photos_count'])
        self.folder_save = self.__get_folder_name('vk_photos', messages['folder_save'])

    @property
    def vk_token(self):
        return self.__vk_token

    @property
    def yandex_token(self):
        return self.__yandex_token
