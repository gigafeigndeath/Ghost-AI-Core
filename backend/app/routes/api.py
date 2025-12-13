from fastapi import APIRouter, Depends, HTTPException  
from pydantic import BaseModel  
from sqlalchemy.orm import Session  
from ..database import SessionLocal, MediaPlan, get_db  
from ..services.parser import parse_article  
from ..services.llm_generator import generate_posts, fallback_posts  
from ..services.image_generator import generate_image  
import logging  

router = APIRouter()  
logging.basicConfig(level=logging.ERROR)  

class UrlRequest(BaseModel):  
    url: str  

@router.post("/analyze/generate_posts")  
def generate_media_plan(request: UrlRequest, db: Session = Depends(get_db)):  
    url = request.url.strip()  
    if not url.startswith("http"):  
        url = "https://" + url  

    article_data = {"title": "Ошибка парсинга", "facts": [], "quotes": [], "numbers": [], "full_text": "", "source_url": url}  
    try:  
        article_data = parse_article(url)  
    except Exception as e:  
        logging.error(f"Ошибка парсинга: {str(e)}")  
        article_data["facts"] = [f"Не удалось загрузить статью: {str(e)}"]  

    posts = fallback_posts(article_data)  
    try:  
        posts = generate_posts(article_data)  
    except Exception as e:  
        logging.error(f"Ошибка LLM: {str(e)}")  

    images = {"telegram": "https://via.placeholder.com/1024?text=Error", "vk": "https://via.placeholder.com/1024?text=Error", "blog": "https://via.placeholder.com/1024?text=Error"}  
    for key in posts:  
        try:  
            images[key] = generate_image(posts[key])  
        except Exception as e:  
            logging.error(f"Ошибка изображения {key}: {str(e)}")  

    try:  
        media_plan = MediaPlan(article_url=url, generated_content=str(posts))  
        db.add(media_plan)  
        db.commit()  
    except Exception as e:  
        logging.error(f"Ошибка БД: {str(e)}")  

    return {"posts": posts, "images": images, "timings": {"telegram": "now", "vk": "in 3-4 hours", "blog": "tomorrow morning"}}  
