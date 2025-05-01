import requests
import os

def download_image(image_url, file_path, timeout=30):
    img_response = requests.get(image_url,timeout=30)
    img_response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(img_response.content)