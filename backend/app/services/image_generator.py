# /var/www/Ghost-AI-Core/backend/app/services/image_generator.py
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-key.fusionbrain.ai/"
API_KEY = os.getenv("KANDINSKY_API_KEY")
SECRET_KEY = os.getenv("KANDINSKY_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise RuntimeError("Не настроены KANDINSKY_API_KEY или KANDINSKY_SECRET_KEY в .env")

AUTH_HEADERS = {
    'X-Key': f'Key {API_KEY}',
    'X-Secret': f'Secret {SECRET_KEY}',
}

def get_pipeline_id():
    """Получаем ID пайплайна (Kandinsky 3.x) — первый в списке"""
    response = requests.get(API_URL + 'key/api/v1/pipelines', headers=AUTH_HEADERS)
    if response.status_code != 200:
        raise ValueError(f"Ошибка получения пайплайнов: {response.status_code} {response.text}")
    pipelines = response.json()
    if not pipelines:
        raise ValueError("Пайплайны не найдены в ответе API")
    return pipelines[0]['id']  # Первый — актуальный Kandinsky

PIPELINE_ID = get_pipeline_id()

def generate_image(prompt: str) -> str:
    if not prompt:
        return "https://via.placeholder.com/1024x1024/333333/ffffff?text=No+Prompt"

    full_prompt = f"Креативная современная иллюстрация к новости в стиле PR-поста: {prompt[:500]}, высокое качество, яркие цвета, минимализм, профессиональный дизайн"

    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": full_prompt}
    }

    data = {
        'pipeline_id': (None, PIPELINE_ID),
        'params': (None, json.dumps(params), 'application/json')
    }

    # Запуск генерации
    response = requests.post(API_URL + 'key/api/v1/pipeline/run', headers=AUTH_HEADERS, files=data)
    if response.status_code != 200:
        return "https://via.placeholder.com/1024x1024/ff4444/ffffff?text=API+Error"

    uuid_val = response.json()['uuid']

    # Ожидание до 75 сек
    attempts = 15
    for _ in range(attempts):
        time.sleep(5)
        status_res = requests.get(API_URL + f'key/api/v1/pipeline/status/{uuid_val}', headers=AUTH_HEADERS)
        if status_res.status_code != 200:
            continue
        data = status_res.json()
        if data['status'] == 'DONE':
            if data.get('censored', False):
                return "https://via.placeholder.com/1024x1024/666666/ffffff?text=Censored"
            # Результат в 'files' или 'images' — берём первый
            result_key = 'files' if 'files' in data.get('result', {}) else 'images'
            images = data.get('result', {}).get(result_key, [])
            if images:
                base64_img = images[0]
                return f"data:image/jpeg;base64,{base64_img}"
            return "https://via.placeholder.com/1024x1024/ff0000/ffffff?text=No+Image"
        elif data['status'] == 'FAILED':
            return "https://via.placeholder.com/1024x1024/ff0000/ffffff?text=Failed"

    return "https://via.placeholder.com/1024x1024/orange/white?text=Timeout"
