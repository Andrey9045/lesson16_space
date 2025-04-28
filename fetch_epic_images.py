import os
import requests
from datetime import datetime, timedelta
import argparse


def download_epic(NASA_API, num_photos=5):
    folder = 'image_epic'
    if not os.path.exists(folder):
        os.makedirs(folder)
    end_date = datetime.now()
    start_date = end_date - timedelta(days = num_photos)
    current_date = start_date
    while  current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f'https://api.nasa.gov/EPIC/api/natural/date/{date_str}?api_key={NASA_API}'
        response = requests.get(url)
        response.raise_for_status()
        epic_info = response.json()
        if epic_info:
            for photo in epic_info[:num_photos]:
                image_name = photo['image']
                image_url = f"https://api.nasa.gov/EPIC/archive/natural/{current_date.year}/{current_date.month:02d}/{current_date.day:02d}/png/{image_name}.png?api_key={NASA_API}"
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                file_path = os.path.join(folder, f"{image_name}.png")
                with open(file_path, 'wb') as file:
                    file.write(image_response.content)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    NASA_API = 'ZeW9HmRtoJXsNJkQA2vXeQHmmSRJjm1gXobuNanS'
    parser = argparse.ArgumentParser(description='Скачает EPIC фото')
    parser.add_argument('--num_photos', type=int, default=5, help='Введите кол-во фото. Дефолтное значение 5')
    args = parser.parse_args()
    download_epic(NASA_API, num_photos=args.num_photos)