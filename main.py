from classes.greeting import Greeting
from classes.vk import Vk
from classes.yandex_disk import YandexDisk


def main():
    greeting = Greeting()
    vk = Vk(greeting.vk_token)
    yandex_disk = YandexDisk(greeting.yandex_token)
    photos = vk.get_photos(greeting.vk_user_id, greeting.photos_count)
    yandex_disk.upload_files(photos, greeting.folder_save)


if __name__ == '__main__':
    main()
