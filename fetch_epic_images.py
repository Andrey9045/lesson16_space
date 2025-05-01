import os
import requests
from datetime import datetime, timedelta
import argparse
from dotenv import load_dotenv
from download_image import download_image

def download_epic(nasa_api, num_photos=5):
    folder = 'image_epic'
    os.makedirs(folder, exist_ok=True)
    end_date = datetime.now()
    start_date = end_date - timedelta(days = num_photos)
    current_date = start_date
    params = {'api_key':nasa_api}
    while  current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f'https://api.nasa.gov/EPIC/api/natural/date/{date_str}'
        response = requests.get(url, params=params)
        response.raise_for_status()
        images = response.json()
        if not images:
            return
        for photo in images[:num_photos]:
            image_name = photo['image']
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{current_date.year}/{current_date.month:02d}/{current_date.day:02d}/png/{image_name}.png"
            file_path = os.path.join(folder, f"{image_name}.png")
            download_image(image_url, file_path, timeout=30)
            

if __name__ == '__main__':
    load_dotenv()
    nasa_api = os.getenv('NASA_API')
    parser = argparse.ArgumentParser(description='Скачает EPIC фото')
    parser.add_argument('--num_photos', type=int, default=5, help='Введите кол-во фото. Дефолтное значение 5')
    args = parser.parse_args()
    download_epic(nasa_api, num_photos=args.num_photos)