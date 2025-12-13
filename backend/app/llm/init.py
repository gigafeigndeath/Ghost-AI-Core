from .yandex_gpt import YandexGPT
from .gigachat import GigaChat
from .ollama import Ollama

def get_llm_client(backend: str):
    if backend == "yandex_gpt":
        return YandexGPT()
    elif backend == "gigachat":
        return GigaChat()
    elif backend == "ollama":
        return Ollama()
    else:
        raise ValueError("Unknown LLM backend")