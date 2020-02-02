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


def get_image_response(url):
    response = requests.get(url=url)
    response.raise_for_status()
    image_response = response.json()
    return image_response


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
    server_response = response.json()
    return server_response


def get_server_data(upload_data):
    server = upload_data['server']
    return server


def get_photo_data(upload_data):
    photo = upload_data['photo']
    return photo


def get_hash_data(upload_data):
    hash_numb = upload_data['hash']
    return hash_numb


def get_id_owner_id(server_response):
    media_id = None
    owner_id = None
    for response in server_response['response']:
        media_id = response['id']
        owner_id = response['owner_id']
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
    image_response = get_image_response(image_url)
    image_title = get_image_title(image_response)
    image_link = get_image_link(image_response)

    filename = get_filename(image_link)
    get_image(image_link, filename, directory)

    vk_uploader_api = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_uploader_params = {'access_token': vk_access_token, 'caption': image_title, 'v': 5.103}
    uploader_url = get_upload_url(vk_uploader_api, vk_uploader_params)

    uploader_response = upload_image_to_group(uploader_url, filename, directory)
    server_response = get_server_data(uploader_response)
    photo_response = get_photo_data(uploader_response)
    hash_response = get_hash_data(uploader_response)

    vk_saver_api = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_saver_params = {'access_token': vk_access_token, 'photo': photo_response, 'server': server_response,
                       'hash': hash_response, 'v': 5.103}
    server_data = save_image_to_group(vk_saver_api, vk_saver_params)
    media_id, owner_id = get_id_owner_id(server_data)

    vk_wall_api = 'https://api.vk.com/method/wall.post'
    vk_wall_params = {'access_token': vk_access_token, 'owner_id': group_id, 'from_group': 1,
                      'message': image_title, 'attachments': f'photo{owner_id}_{media_id}', 'v': 5.103}
    post_wall(vk_wall_api, vk_wall_params)
    remove_image(filename, directory)


if __name__ == '__main__':
    main()
