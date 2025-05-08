import os
import requests
import argparse
from download_image import download_image


def fetch_spacex_images(launch_url, folder):
    response = requests.get(launch_url)
    response.raise_for_status()
    images = response.json()
    if 'error' in images:
        raise requests.exceptions.HTTPError(decoded_response['error'])
    
    image_links = []
    if 'links' in images and 'flickr' in images['links']:
        image_links.extend(images['links']['flickr']['original'])
    
    os.makedirs(folder, exist_ok=True)
    
    for index, image_url in enumerate(image_links, start=1):
        filename = f"spacex{index}.jpeg"
        file_path = os.path.join(folder, filename)
        download_image(image_url, file_path, timeout=30)
    
    print(f"Downloaded {len(image_links)} images to '{folder}'.")

def main():
    parser = argparse.ArgumentParser(description="Download SpaceX launch images.")
    parser.add_argument(
        '--launch_id', 
        type=str,
        default=None, 
        help='The ID of the SpaceX launch to download images from. If not provided, the latest launch images will be downloaded.'
    )
    
    args = parser.parse_args()
    spacex_url = "https://api.spacexdata.com/v4/launches"
    folder = "spacex_images"
    launch_id = args.launch_id

    if launch_id:
        launch_url = f"{spacex_url}/{launch_id}"
    else:
        last_launch_response = requests.get(f"{spacex_url}/latest")
        last_launch_response.raise_for_status()
        last_launch = last_launch_response.json()
        launch_url = f"{spacex_url}/{last_launch['id']}"

    fetch_spacex_images(launch_url, folder)

if __name__ == "__main__":
    main()
