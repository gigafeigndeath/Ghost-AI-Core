from app.config import settings
import requests  # Предполагаем, что requests в requirements

class YandexGPT:
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY

    def generate(self, prompt: str):
        # Упрощенная интеграция
        response = requests.post("https://api.yandexgpt.com/generate", json={"prompt": prompt}, headers={"Authorization": self.api_key})
        return response.json().get("text", "Error")