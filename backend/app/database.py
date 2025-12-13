from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  
from sqlalchemy import Column, Integer, String  
from dotenv import load_dotenv  
import os  

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pr_agent.db")  # Fallback на sqlite  

engine = create_engine(DATABASE_URL)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()  

class MediaPlan(Base):  
    __tablename__ = "media_plans"  
    id = Column(Integer, primary_key=True, index=True)  
    article_url = Column(String, index=True)  
    generated_content = Column(String)  

Base.metadata.create_all(bind=engine)  

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()  
