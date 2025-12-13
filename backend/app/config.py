from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ghost_ai.db"
    YANDEX_GPT_API_KEY: Optional[str] = None
    GIGACHAT_API_KEY: Optional[str] = None
    OLLAMA_MODEL: str = "llama3"
    KANDINSKY_API_KEY: Optional[str] = None
    STABLE_DIFFUSION_API_URL: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    VK_API_TOKEN: Optional[str] = None
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()