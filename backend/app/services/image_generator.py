import requests
from . import config

def generate_image(prompt: str) -> str:
    # API Kandinsky (адаптируй под актуальный endpoint; это пример)
    url = "https://api.kandinsky.sber.ai/v1/generate"  # Проверь актуальный URL в docs Sber
    headers = {
        "Authorization": f"Bearer {config.KANDINSKY_API_KEY}:{config.KANDINSKY_SECRET_KEY}"
    }
    data = {
        "prompt": prompt,
        "style": "default",  # Или другие опции
        "num_images": 1
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["images"][0]["url"]  # Возвращаем URL сгенерированного изображения
    return "Error generating image"
