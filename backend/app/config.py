from dotenv import load_dotenv
import os

load_dotenv()

GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

KANDINSKY_API_KEY = os.getenv("KANDINSKY_API_KEY")
KANDINSKY_SECRET_KEY = os.getenv("KANDINSKY_SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pr_agent.db")
