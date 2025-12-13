from app.config import settings
import requests

class GigaChat:
    def __init__(self):
        self.api_key = settings.GIGACHAT_API_KEY

    def generate(self, prompt: str):
        # Упрощенная интеграция
        response = requests.post("https://api.gigachat.com/chat", json={"prompt": prompt}, headers={"Authorization": self.api_key})
        return response.json().get("response", "Error")