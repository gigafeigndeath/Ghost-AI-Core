import asyncio
import schedule
import time
import requests
from bs4 import BeautifulSoup
from aiogram import Bot
from vk_api import VkApi
from vk_api.upload import VkUpload
# Твой GigaChat/LangChain для реврайта

# .env токены
TELEGRAM_TOKEN = '8343473188:AAGv2jGmWNIRBVt9nd_GbViTx3pY2dj9fqE'
VK_TOKEN = '...'
VK_GROUP_ID = -123456  # ID группы

bot = Bot(token=TELEGRAM_TOKEN)
vk_session = VkApi(token=VK_TOKEN)
vk_upload = VkUpload(vk_session)

async def generate_and_post(article_url):
    # 1. Парсинг
    html = requests.get(article_url).text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.h1.text if soup.h1 else 'Новость'
    facts = ' '.join([p.text for p in soup.find_all('p')[:5]])

    # 2. Генерация постов via GigaChat (твой код)
    posts = {
        'telegram': f"⚡ Срочно! {title} {article_url}",  # Коротко, факты
        'vk': f"😎 Привет! Интересный факт: {facts[:200]}... Подробности: {article_url}",  # Дружелюбно, эмодзи
        'vc': f"Бизнес-успех: {title}. Цифры и анализ: {facts} Источник: {article_url}"  # Профессионально
    }

    # 3. Картинка Kandinsky (API Сбер)
    img_prompt = f"Креативная иллюстрация к новости: {title}"
    img_url = requests.post('https://api.sber.ai/v1/kandinsky/generate', json={'prompt': img_prompt, 'api_key': 'YOUR_KEY'}).json()['image']

    # 4. Постинг с таймингом
    # Telegram сразу
    await bot.send_photo('@your_channel', img_url, caption=posts['telegram'])

    # VK через 3-4 часа
    schedule.every(3).hours.do(lambda: vk_session.method('wall.post', {'owner_id': VK_GROUP_ID, 'message': posts['vk'], 'attachments': vk_upload.photo_wall(photos=img_url)[0]} ))

    # VC — вручную или через другой API (утро)

    while True:
        schedule.run_pending()
        time.sleep(60)

# В routes: вызов по URL из фронта
