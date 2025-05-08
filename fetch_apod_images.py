import os
import requests
from urllib.parse import urlsplit, unquote
import argparse
from dotenv import load_dotenv
from download_image import download_image

def get_an_extension(image_url):
    parsed_url = urlsplit(image_url)
    path = unquote(parsed_url.path)
    filename = os.path.split(path)[-1]
    slash, extension = os.path.splitext(filename)
    return extension

def download_apod(nasa_key, count=30):
    params = {
        'api_key': nasa_key,
        'count': count
    }
    url = f'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=params)
    response.raise_for_status() 
    images = response.json()
    folder = 'image_apod'
    os.makedirs(folder, exist_ok=True)
    for index, image in enumerate(images, start=1):
        image_url = image['url']
        if not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"Пропускаем URL (не изображение): {image_url}")
            continue
        extension = get_an_extension(image_url)
        filename = f"apod{index}{extension}"
        file_path = os.path.join(folder, filename)
        download_image(image_url, file_path, timeout=30)

if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.getenv('NASA_KEY')
    parser = argparse.ArgumentParser(description='Download images from NASA APOD.')
    parser.add_argument('--count', type=int, default=30, help='Number of images to download (default: 30).')

    args = parser.parse_args()
    
    download_apod(nasa_key, count=args.count)
    