from app.config import settings
# Предполагаем ollama библиотеку или HTTP

class Ollama:
    def __init__(self):
        self.model = settings.OLLAMA_MODEL

    def generate(self, prompt: str):
        # Упрощенная локальная интеграция (требует ollama running)
        import ollama  # ollama package
        return ollama.generate(model=self.model, prompt=prompt)['response']