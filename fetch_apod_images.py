import os
import requests
from urllib.parse import urlsplit, unquote
import argparse

def get_file_extensionget_file_extension(image_url):
    parsed_url = urlsplit(image_url)
    path = unquote(parsed_url.path)
    filename = os.path.split(path)[-1]
    slash, extension = os.path.splitext(filename)
    return extension

def download_apod(NASA_API, count=30):
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API}&count={count}'
    response = requests.get(url)
    response.raise_for_status()
    images = response.json()
    folder = 'image_apod'
    if not os.path.exists(folder):
        os.makedirs(folder)
    for index, image in enumerate(images, start=1):
        image_url = image['url']
        if not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"Пропускаем URL (не изображение): {image_url}")
            continue
        extension = get_file_extensionget_file_extension(image_url)
        filename = f"apod{index}{extension}"
        file_path = os.path.join(folder, filename)
        img_response = requests.get(image_url,timeout=30)
        img_response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(img_response.content)

if __name__ == '__main__':
    NASA_API = 'ZeW9HmRtoJXsNJkQA2vXeQHmmSRJjm1gXobuNanS'
    parser = argparse.ArgumentParser(description='Download images from NASA APOD.')
    parser.add_argument('--count', type=int, default=30, help='Number of images to download (default: 30).')

    args = parser.parse_args()
    
    download_apod(NASA_API, count=args.count)
    