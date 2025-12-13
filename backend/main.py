import os
from fastapi import FastAPI, Body
from dotenv import load_dotenv
from utils import parse_article, generate_posts

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Ghost-AI-Core Backend",
    description="Autonomous PR AI agent for МПИТ contest: Extends news lifespan by generating multi-platform content."
)

@app.post("/process_article")
def process_article(url: str = Body(...)):
    posts = generate_posts(url)
    return posts
