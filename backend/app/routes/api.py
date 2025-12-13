from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel  # ← Добавь импорт для UrlRequest
from sqlalchemy.orm import Session
from ..database import SessionLocal, MediaPlan
from ..services.parser import parse_article
from ..services.llm_generator import generate_posts
from ..services.image_generator import generate_image

router = APIRouter()

class UrlRequest(BaseModel):  # ← Модель для body {"url": "..."}
    url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze/generate_posts")  # ← Новый путь для фронта
def generate_media_plan(request: UrlRequest, db: Session = Depends(get_db)):
    url = request.url  # Берём из body
    if not url.startswith("http"):  # ← Фикс: добавляем https если забыли
        url = "https://" + url

    try:
        article_data = parse_article(url)
        posts = generate_posts(article_data)
        
        # Генерация изображений для каждого поста
        images = {
            "telegram": generate_image(f"Иллюстрация для поста: {posts['telegram']}"),
            "vk": generate_image(f"Иллюстрация для поста: {posts['vk']}"),
            "blog": generate_image(f"Иллюстрация для поста: {posts['blog']}")
        }
        
        # Сохранение в БД
        media_plan = MediaPlan(article_url=url, generated_content=str(posts))
        db.add(media_plan)
        db.commit()
        
        # Возврат медиаплана
        return {
            "posts": posts,
            "images": images,
            "timings": {
                "telegram": "now",
                "vk": "in 3-4 hours",
                "blog": "tomorrow morning"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")

# Оставь /publish как есть
@router.post("/publish")
def publish(post_type: str, content: str):
    # Твой код автопостинга
    return {"status": "published"}
