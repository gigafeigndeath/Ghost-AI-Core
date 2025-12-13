from .base import Base
from .article import Article
from .post import Post
from .user import User

Base = Article.__bases__[0]  # Assuming declarative_base
