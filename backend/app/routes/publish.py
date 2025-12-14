# /var/www/Ghost-AI-Core/backend/app/routes/publish.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
import base64
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class PublishRequest(BaseModel):
    post_type: str
    content: str
    image_url: str | None = None

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError("Не настроены TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID в .env")

@router.post("/publish")
async def publish(request: PublishRequest):
    if request.post_type != "telegram":
        raise HTTPException(400, "Автопостинг сейчас только в Telegram")

    text = request.content.strip()

    # Убрали добавление "Источник:" — ссылка уже в тексте поста от LLM

    async with httpx.AsyncClient() as client:
        # Если есть нормальная base64-картинка от Kandinsky — отправляем фото + подпись
        if request.image_url and request.image_url.startswith("data:image"):
            base64_str = request.image_url.split(",", 1)[1]
            try:
                photo_bytes = base64.b64decode(base64_str)
            except:
                # Если base64 сломан — отправляем просто текст
                photo_bytes = None

            if photo_bytes:
                files = {"photo": ("ghost-ai.jpg", photo_bytes, "image/jpeg")}
                data = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": text,
                    "parse_mode": "HTML"
                }
                response = await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                    data=data,
                    files=files,
                    timeout=40
                )
            else:
                raise ValueError("Invalid image")
        else:
            # Просто текст (если картинки нет или ошибка)
            params = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            response = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                params=params,
                timeout=20
            )

        if response.status_code != 200:
            error = response.json().get("description", response.text)
            raise HTTPException(500, f"Ошибка Telegram: {error}")

    return {"status": "published", "platform": "telegram"}
