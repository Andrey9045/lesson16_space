import os
import random
import time
import argparse
from telegram import Bot
from dotenv import load_dotenv

def send_image(bot, image_path):
    with open(image_path, 'rb') as image_file:
        bot.send_photo(chat_id=channel_id, photo=image_file)

def publish_images(directory, delay):
    bot = Bot(token=bot_token)
    all_files = os.listdir(directory)
    images = []
    for picture in all_files:
        if picture.endswith(('.jpg', '.jpeg', '.png')):
        	images.append(picture)
    
    if not images:
        print("Нет изображений для публикации.")
        return

    while True:
        random.shuffle(images)  
        for image in images:
            image_path = os.path.join(directory, image)
            send_image(bot, image_path)
            time.sleep(delay)

if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    channel_id = os.getenv('CHANNEL_ID')
    parser = argparse.ArgumentParser(description='Публикация изображений в Telegram-канал.')
    parser.add_argument('directory', type=str, help='Директория с изображениями для публикации')
    parser.add_argument('--delay', type=int, default=14400, help='Задержка между публикациями в секундах (по умолчанию 4 часа)')
    
    args = parser.parse_args()
    
    publish_images(args.directory, args.delay)
