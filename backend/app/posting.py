import os
import logging
from typing import Optional

class MockPoster:
    """Заглушка для автопостинга — логирует посты (для теста)."""
    def post(self, platform: str, text: str, image_url: Optional[str] = None):
        logging.info(f"[MOCK POST] Платформа: {platform}")
        logging.info(f"Текст: {text}")
        if image_url:
            logging.info(f"Картинка: {image_url}")
        return {"status": "posted", "platform": platform, "url": "https://example.com/mock-post (МПИТ)"}

def get_poster(poster_type: str = "mock"):
    """Фабрика постеров."""
    return MockPoster()  # По умолчанию заглушка — работает сразу

def post_to_platform(platform: str, text: str, image_url: Optional[str] = None):
    """Прямая функция публикации — используется в API."""
    poster = get_poster()
    return poster.post(platform, text, image_url)
