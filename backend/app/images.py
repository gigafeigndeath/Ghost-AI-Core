import os
import logging
from typing import Optional

class MockImageGenerator:
    """Заглушка для генерации изображений — возвращает placeholder (для теста)."""
    def generate(self, prompt: str) -> str:
        placeholder = f"https://via.placeholder.com/1024x768/3366FF/FFFFFF?text={prompt[:60].replace(' ', '+')}+(МПИТ)"
        logging.info(f"[MOCK IMAGE] Промпт: {prompt} → {placeholder}")
        return placeholder

def get_image_generator(generator_type: str = "mock"):
    """Фабрика генераторов изображений."""
    return MockImageGenerator()  # По умолчанию заглушка — работает сразу

def generate_image(prompt: str, generator_type: str = "mock") -> str:
    """Прямая функция генерации изображения — используется в API."""
    generator = get_image_generator(generator_type)
    return generator.generate(prompt)
