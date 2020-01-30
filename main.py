import requests
import os
from dotenv import load_dotenv
from random import randint


def make_directory(directory):
    os.makedirs(directory, exist_ok=True)


def get_image(image_link, filename, directory):
    full_filename = directory + filename
    response = requests.get(image_link)
    response.raise_for_status()

    with open(full_filename, 'wb') as file:
        file.write(response.content)


def get_image_data(url):
    response = requests.get(url=url)
    response.raise_for_status()
    image_data = response.json()
    return image_data


def get_filename(image_link):
    head, tail = os.path.split(image_link)
    return tail


def get_image_link(image_data):
    image_link = image_data['img']
    return image_link


def get_image_title(image_data):
    image_title = image_data['title']
    return image_title


def get_upload_url(vk_get_groups_url, vk_get_group_params):
    response = requests.get(url=vk_get_groups_url, params=vk_get_group_params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_image_to_group(upload_url, filename, directory):
    full_file = directory + filename

    with open(full_file, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server_result = response.json()
    return server_result


def save_image_to_group(vk_save_image_api, vk_save_params):
    response = requests.post(url=vk_save_image_api, params=vk_save_params)
    response.raise_for_status()
    server_data = response.json()
    return server_data


def get_server_data(upload_data):
    server_data = upload_data['server']
    return server_data


def get_photo_data(upload_data):
    photo_data = upload_data['photo']
    return photo_data


def get_hash_data(upload_data):
    hash_data = upload_data['hash']
    return hash_data


def get_id_owner_id(server_data):
    media_id = None
    owner_id = None
    for item in server_data['response']:
        media_id = item['id']
        owner_id = item['owner_id']
    return media_id, owner_id


def post_wall(vk_wall_post_api, vk_wall_post_params):
    response = requests.post(vk_wall_post_api, vk_wall_post_params)
    response.raise_for_status()


def remove_image(filename, directory):
    full_name = directory + filename
    os.remove(full_name)


def main():
    load_dotenv(verbose=True)
    group_id = os.getenv('GROUP_ID')
    vk_access_token = os.getenv('ACCESS_TOKEN')
    directory = 'image/'

    make_directory(directory)

    numb = randint(1, 2261)
    image_url = f'http://xkcd.com/{numb}/info.0.json'
    image_data = get_image_data(image_url)
    image_title = get_image_title(image_data)
    image_link = get_image_link(image_data)

    filename = get_filename(image_link)
    get_image(image_link, filename, directory)

    vk_uploader_api = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_uploader_params = {'access_token': vk_access_token, 'caption': image_title, 'v': 5.103}
    uploader_url = get_upload_url(vk_uploader_api, vk_uploader_params)

    uploader_data = upload_image_to_group(uploader_url, filename, directory)
    server_data = get_server_data(uploader_data)
    photo_data = get_photo_data(uploader_data)
    hash_data = get_hash_data(uploader_data)

    vk_saver_api = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_saver_params = {'access_token': vk_access_token, 'photo': photo_data, 'server': server_data,
                       'hash': hash_data, 'v': 5.103}
    server_data = save_image_to_group(vk_saver_api, vk_saver_params)
    media_id, owner_id = get_id_owner_id(server_data)

    vk_wall_api = 'https://api.vk.com/method/wall.post'
    vk_wall_params = {'access_token': vk_access_token, 'owner_id': group_id, 'from_group': 1,
                      'message': image_title, 'attachments': f'photo{owner_id}_{media_id}', 'v': 5.103}
    post_wall(vk_wall_api, vk_wall_params)
    remove_image(filename, directory)


if __name__ == '__main__':
    main()
