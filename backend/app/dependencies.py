from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.llm import get_llm_client
from app.parsers import get_parser
from app.images import get_image_generator
from app.posting import get_poster

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_llm(backend: str = "yandex_gpt"):
    return get_llm_client(backend)

def get_article_parser(method: str = "bs4"):
    return get_parser(method)

def get_image_gen(method: str = "kandinsky"):
    return get_image_generator(method)

def get_poster(platform: str = "telegram"):
    return get_poster(platform)