import os
import requests
import argparse
from creating_a_folder import creating_a_folder

def fetch_spacex_images(launch_url, folder):
    response = requests.get(launch_url)
    launch_data = response.json()
    
    image_links = []
    if 'links' in launch_data and 'flickr' in launch_data['links']:
        image_links.extend(launch_data['links']['flickr']['original'])
    
    creating_a_folder(folder)
    
    for index, image_link in enumerate(image_links, start=1):
        filename = f"spacex{index}.jpeg"
        file_path = os.path.join(folder, filename)
        img_response = requests.get(image_link)
        img_response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(img_response.content)
    
    print(f"Downloaded {len(image_links)} images to '{folder}'.")

def main(launch_id=None):
    spacex_url = "https://api.spacexdata.com/v4/launches"
    folder = "spacex_images"

    if launch_id:
        launch_url = f"{spacex_url}/{launch_id}"
    else:
        last_launch_response = requests.get(f"{spacex_url}/latest")
        last_launch = last_launch_response.json()
        launch_url = f"{spacex_url}/{last_launch['id']}"

    fetch_spacex_images(launch_url, folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download SpaceX launch images.")
    parser.add_argument(
        '--launch_id', 
        type=str, 
        help='The ID of the SpaceX launch to download images from. If not provided, the latest launch images will be downloaded.'
    )
    
    args = parser.parse_args()
    main(args.launch_id)
