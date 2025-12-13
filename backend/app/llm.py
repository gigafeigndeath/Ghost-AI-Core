class MockLLM:
    """Mock LLM с отметкой конкурса МПИТ для стабильности демо."""
    def invoke(self, prompt: str) -> str:
        return f"Участник конкурса МПИТ: рерайт новости — {prompt[:300]}... (полный текст в продакшене с YandexGPT/GigaChat)"

def get_llm_client(backend: str | None = None):
    """Фабрика LLM — принимает backend, но всегда возвращает mock для конкурса МПИТ."""
    # Если backend == "yandex" или "giga" — здесь можно добавить реальный код с ключами из .env
    # Пока mock — 100% стабильность
    return MockLLM()
