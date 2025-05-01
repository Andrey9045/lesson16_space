import os
import random
import time
import argparse
from telegram import Bot
from dotenv import load_dotenv

def send_image(bot, path, channel_id):
    with open(path, 'rb') as image_file:
        bot.send_photo(chat_id=channel_id, photo=image_file)

def publish_images(path, delay, bot_token, channel_id):
    bot = Bot(token=bot_token)
    if os.path.isfile(path):
        send_image(bot, path, channel_id)
        return
    all_files = os.listdir(path)
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
            path = os.path.join(path, image)
            send_image(bot, path, channel_id)
            time.sleep(delay)

if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('TG_BOT_TOKEN')
    channel_id = os.getenv('TG_CHANNEL_ID')
    parser = argparse.ArgumentParser(description='Публикация изображений в Telegram-канал.')
    parser.add_argument('path', type=str, help='Директория с изображениями для публикации')
    parser.add_argument('--delay', type=int, default=14400, help='Задержка между публикациями в секундах (по умолчанию 4 часа)')
    
    args = parser.parse_args()
    
    publish_images(args.path, args.delay, bot_token, channel_id)

