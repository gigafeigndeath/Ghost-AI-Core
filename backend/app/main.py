from fastapi import FastAPI
from .routes.api import router as api_router  # Connect router from routes/api.py (english comment)
from .routes.publish import router as publish_router

app = FastAPI(
    title="PR AI Agent Backend",
    description="Автономный PR-агент: парсит статьи, генерит посты для Telegram/VK/VC с таймингом и картинками Kandinsky",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router)  # Без prefix — nginx добавит /api/
app.include_router(publish_router)
