from app.config import settings
import requests

def generate_with_kandinsky(prompt: str, style: str):
    # Упрощенная интеграция
    response = requests.post("https://api.kandinsky.sber.ru/generate", json={"prompt": prompt, "style": style}, headers={"Authorization": settings.KANDINSKY_API_KEY})
    return response.json().get("image_url", "Error")