from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    platform = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))