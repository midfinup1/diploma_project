import requests
import os
import tqdm
import json
import shutil


class Vk:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_profile_pics(self):
        VK_TOKEN = vk_token_input
        API_BASE_URL = 'https://api.vk.com/method/'
        V = '5.124'
        ALBUM_ID = 'profile'
        OWNER_ID = user_id_input
        photos_get_url = (API_BASE_URL + 'photos.get')
        response = requests.get(photos_get_url, params={
            'access_token': VK_TOKEN,
            'v': V,
            'album_id': ALBUM_ID,
            'owner_id': OWNER_ID,
            'extended': 1
        })
        os.mkdir("temp_folder")
        photo_name_list = []
        count = response.json()['response']['count']
        for items in response.json()['response']['items']:
            photo_name = items['likes']['count']
            if photo_name in photo_name_list:
                photo_name = str(photo_name) + '_' + str(items['date'])
            photo_name_list.append(photo_name)
            max_value = 0
            temp_dict = {}
            file_to_upload = []
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
            filename = "temp_folder" + f"/{photo_name}.txt"
            with open(filename, "w") as f:
                f.write(json.dumps(file_to_upload))
            count = 5
        return photo_name_list, count


class Yandex:
    def __init__(self, token: str):
        self.token = token

    def upload(self):
        response = Vk.get_profile_pics(user_id_input)
        photo_name_list = response[0]
        count = response[1]
        HEADERS = {"Authorization": f"OAuth {self.token}"}
        data = {'path': 'Netology_folder'}
        data_name = data['path']
        requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=HEADERS, params=data)
        for i in tqdm.tqdm(range(0, count)):
            photo_name = photo_name_list[i]
            data = {'path': f'{data_name}/{photo_name}.jpg'}
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
                                    params=data)
            ya_disk_url = response.json()['href']
            filename = "temp_folder" + f"/{photo_name}.jpg"
            files = {'file': open(filename, 'rb')}
            requests.post(ya_disk_url, files=files)
            data = {'path': f'{data_name}/{photo_name}.txt'}
            filename = "temp_folder" + f"/{photo_name}.txt"
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
                                    params=data)
            ya_disk_url = response.json()['href']
            files = {'file': open(filename, 'rb')}
            requests.post(ya_disk_url, files=files)
        return 'Done'


if __name__ == '__main__':
    user_id_input = input('Введите id профиля: ')
    yandex_token_input = input('Введите свой яндекс токен: ')
    vk_token_input = input('Введите свой токен ВК: ')
    uploader = Yandex(yandex_token_input)
    result = uploader.upload()
    print(result)
    shutil.rmtree("temp_folder")
