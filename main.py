import requests
import os
import tqdm
import json
import shutil


class Vk:
    def __init__(self, user_id: str, token_vk: str):
        self.user_id = input('Введите id профиля: ')
        self.token_id = input('Введите токен ВК: ')

    def get_profile_pics(self):
        VK_TOKEN = self.token_id
        API_BASE_URL = 'https://api.vk.com/method/'
        V = '5.124'
        ALBUM_ID = 'profile'
        USER_ID = self.user_id
        photos_get_url = (API_BASE_URL + 'photos.get')
        response = requests.get(photos_get_url, params={
            'access_token': VK_TOKEN,
            'v': V,
            'album_id': ALBUM_ID,
            'owner_id': USER_ID,
            'extended': 1
        })
        os.mkdir("temp_folder")
        photo_name_list = []
        file_to_upload = []
        count = response.json()['response']['count']
        for items in response.json()['response']['items']:
            photo_name = items['likes']['count']
            if photo_name in photo_name_list:
                photo_name = str(photo_name) + '_' + str(items['date'])
            photo_name_list.append(photo_name)
            max_value = 0
            temp_dict = {}
            for item in items['sizes']:
                if item['width'] > max_value:
                    max_value = item['width']
                    size = item['type']
                    photo_url = item['url']
            temp_dict['file_name'] = str(photo_name) + '.jpg'
            temp_dict['size'] = size
            file_to_upload.append(temp_dict)
            img = requests.get(photo_url)
            filename = "temp_folder" + f"/{photo_name}.jpg"
            with open(filename, "wb") as f:
                f.write(img.content)
        filename = "temp_folder" + '/' + "all_photos.txt"
        with open(filename, "w") as f:
            f.write(json.dumps(file_to_upload))


class Yandex:
    def __init__(self, token: str):
        self.token = input('Введите свой токен Яндекс: ')

    def upload(self, download_folder: str, upload_folder: str):
        download_folder = "temp_folder"
        data = {'path': 'Netology_folder'}
        upload_folder = data['path']
        HEADERS = {"Authorization": f"OAuth {self.token}"}
        requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=HEADERS, params=data)
        count = 5
        for i in tqdm.tqdm(range(0, count)):
            photo_name = os.listdir(download_folder)[i].split('.')[0]
            data = {'path': f'{upload_folder}/{photo_name}.jpg'}
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
                                    params=data)
            ya_disk_url = response.json()['href']
            filename = "temp_folder" + f"/{photo_name}.jpg"
            files = {'file': open(filename, 'rb')}
            requests.post(ya_disk_url, files=files)
        data = {'path': f'{upload_folder}/all_photos.txt'}
        filename = "temp_folder" + "/" + "all_photos.txt"
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
                                params=data)
        ya_disk_url = response.json()['href']
        files = {'file': open(filename, 'rb')}
        requests.post(ya_disk_url, files=files)
        print('Done')


user = Vk('', '')
user.get_profile_pics()
user1 = Yandex('')
user1.upload('', '')
shutil.rmtree('temp_folder')
