import requests
import os
import urllib.request
import tqdm
import json

class Vk:
    def __init__(self, owner_id: str):
        self.owner_id = owner_id

    def get_profile_pics(self):
        VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
        API_BASE_URL = 'https://api.vk.com/method/'
        V = '5.124'
        ALBUM_ID = 'profile'
        OWNER_ID = self.owner_id
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
        for items in tqdm.tqdm(response.json()['response']['items']):
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
                    photo_to_save = item['url']
            temp_dict['file_name'] = str(photo_name) + '.jpg'
            temp_dict['size'] = size
            file_to_upload.append(temp_dict)
            img = urllib.request.urlopen(photo_to_save).read()
            filename = "temp_folder" + f"/{photo_name}.jpg"
            with open(filename, "wb") as f:
                f.write(img)
            with open(filename, "w") as f:
                f.write(json.dumps(file_to_upload))
            count = 5
            return photo_name, count


class Yandex:
    def __init__(self, token: str):
        self.token = token

    def upload(self):
        count = Vk.get_profile_pics()[1]
        for i in range(0, count):
            photo_name = Vk.get_profile_pics()[0]
            HEADERS = {"Authorization": f"OAuth {self.token}"}
            data = {'path': 'Netology_folder'}
            data_name = data['path']
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


class User:
    def __init__(self, token: str, owner_id: str):
        self.token = token
        self.owner_id = owner_id

    def upload(self):
        count = Vk.get_profile_pics()[1]
        for i in range(0, count):
            Yandex.upload()
        return 'Done'


if __name__ == '__main__':
    owner_id_input = input('Введите id профиля: ')
    token_input = input('Введите свой токен: ')
    uploader = User(token_input, owner_id_input)
    result = uploader.upload()
    print(result)





# class User:
#     def __init__(self, token: str, owner_id: str):
#         self.token = token
#         self.owner_id = owner_id
#
#     def upload(self):
#         HEADERS = {"Authorization": f"OAuth {self.token}"}
#         data = {'path': 'Netology_folder'}
#         data_name = data['path']
#         requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=HEADERS, params=data)
#         VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
#         API_BASE_URL = 'https://api.vk.com/method/'
#         V = '5.124'
#         ALBUM_ID = 'profile'
#         OWNER_ID = self.owner_id
#         photos_get_url = (API_BASE_URL + 'photos.get')
#         response = requests.get(photos_get_url, params={
#             'access_token': VK_TOKEN,
#             'v': V,
#             'album_id': ALBUM_ID,
#             'owner_id': OWNER_ID,
#             'extended': 1
#         })
#         os.mkdir("temp_folder")
#         photo_name_list = []
#         for items in tqdm.tqdm(response.json()['response']['items']):
#             photo_name = items['likes']['count']
#             if photo_name in photo_name_list:
#                 photo_name = str(photo_name) + '_' + str(items['date'])
#             photo_name_list.append(photo_name)
#             max_value = 0
#             temp_dict = {}
#             file_to_upload = []
#             for item in items['sizes']:
#                 if item['width'] > max_value:
#                     max_value = item['width']
#                     size = item['type']
#                     photo_to_save = item['url']
#             temp_dict['file_name'] = str(photo_name) + '.jpg'
#             temp_dict['size'] = size
#             file_to_upload.append(temp_dict)
#             img = urllib.request.urlopen(photo_to_save).read()
#             data = {'path': f'{data_name}/{photo_name}.jpg'}
#             filename = "temp_folder" + f"/{photo_name}.jpg"
#             with open(filename, "wb") as f:
#                 f.write(img)
#             response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
#                                     params=data)
#             ya_disk_url = response.json()['href']
#             files = {'file': open(filename, 'rb')}
#             requests.post(ya_disk_url, files=files)
#             # os.remove(filename)
#             data = {'path': f'{data_name}/{photo_name}.txt'}
#             filename = "temp_folder" + f"/{photo_name}.txt"
#             with open(filename, "w") as f:
#                 f.write(json.dumps(file_to_upload))
#             response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=HEADERS,
#                                     params=data)
#             ya_disk_url = response.json()['href']
#             files = {'file': open(filename, 'rb')}
#             requests.post(ya_disk_url, files=files)
#             # os.remove(filename)
#             # os.rmdir(path)
#         return 'Done'
#
#
# if __name__ == '__main__':
#     owner_id_input = input('Введите id профиля: ')
#     token_input = input('Введите свой токен: ')
#     uploader = User(token_input, owner_id_input)
#     result = uploader.upload()
#     print(result)
user = Yandex('AgAAAAAa6zIQAADLW7XGfiL5V03inKkQ2URzD6o')
print(Yandex.upload(user))