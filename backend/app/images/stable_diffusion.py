from app.config import settings
import requests

def generate_with_sd(prompt: str, style: str):
    # Предполагаем API endpoint
    response = requests.post(settings.STABLE_DIFFUSION_API_URL, json={"prompt": prompt, "style": style})
    return response.json().get("image_url", "Error")