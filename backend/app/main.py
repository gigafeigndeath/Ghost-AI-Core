from fastapi import FastAPI
from app.api import analyze, media, health, publish
from app.db.session import engine
# from app.models import Base

# Создаем таблицы в БД при запуске
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ghost AI PR Agent",
    description="Автономный ИИ-агент для продления жизни инфоповодов. Участие в конкурсе МПИТ.",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(publish.router, prefix="/api/publish", tags=["publish"])

@app.get("/")
def root():
    return {"message": "Welcome to Ghost AI PR Agent! Автоматизируйте PR и сломайте алгоритмы охватов."}
