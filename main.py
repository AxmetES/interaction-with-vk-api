import requests
import os
from dotenv import load_dotenv


def make_directory(directory):
    os.makedirs(directory, exist_ok=True)


def get_image(image_link, filename, directory):
    full_filename = directory + filename
    response = requests.get(image_link)
    response.raise_for_status()

    with open(full_filename, 'wb') as file:
        file.write(response.content)


def get_data(url):
    response = requests.get(url=url)
    response.raise_for_status()
    image_data = response.json()
    return image_data


def get_filename(image_link):
    head, tail = os.path.split(image_link)
    return tail


def get_description(image_data):
    description = image_data['alt']
    return description


def get_image_link(image_data):
    image_link = image_data['img']
    return image_link


def get_vk_group(vk_get_groups_url, vk_get_group_params):
    response = requests.get(url=vk_get_groups_url, params=vk_get_group_params)
    groups = response.json()['response']['items']
    print(groups)


def main():
    client_id = os.getenv('CLIENT_ID')
    vk_access_token = os.getenv('ACCESS_TOKEN')
    load_dotenv(verbose=True)
    directory = 'image/'
    image_url = 'http://xkcd.com/info.0.json'
    make_directory(directory)
    vk_get_groups_url = 'https://api.vk.com/method/photos.getWallUploadServer '
    vk_get_group_params = {'access_token': vk_access_token, 'v': 5.103}

    image_data = get_data(image_url)
    description = get_description(image_data)
    image_link = get_image_link(image_data)
    filename = get_filename(image_link)
    get_image(image_link, filename, directory)
    print(description)

    get_vk_group(vk_get_groups_url, vk_get_group_params)


if __name__ == '__main__':
    main()
