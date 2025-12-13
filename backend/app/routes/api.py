from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal, MediaPlan
from ..services.parser import parse_article
from ..services.llm_generator import generate_posts
from ..services.image_generator import generate_image

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
def generate_media_plan(url: str, db: Session = Depends(get_db)):
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
    
    # Возвращаем медиаплан (фронтенд может отобразить)
    return {
        "posts": posts,
        "images": images,
        "timings": {
            "telegram": "now",
            "vk": "in 3-4 hours",
            "blog": "tomorrow morning"
        }
    }

# Заглушка для автопостинга (расширь)
@router.post("/publish")
def publish(post_type: str, content: str):
    if post_type == "telegram":
        # Здесь интеграция с Telegram API
        pass
    # Аналогично для VK и блога
    return {"status": "published"}
