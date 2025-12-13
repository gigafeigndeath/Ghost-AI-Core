from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Пример модели для хранения медиапланов (расширь по нужде)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class MediaPlan(Base):
    __tablename__ = "media_plans"
    id = Column(Integer, primary_key=True, index=True)
    article_url = Column(String, index=True)
    generated_content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
