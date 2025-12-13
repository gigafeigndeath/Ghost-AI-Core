import requests
from .. import config

def generate_image(prompt: str) -> str:
    # Фолбэк: возвращаем заглушку вместо реальной генерации
    return f"https://via.placeholder.com/1024x1024.png?text=Иллюстрация: {prompt[:50]}..."  # Плейсхолдер
    # Или локальный URL: return "/static/placeholder.jpg"
