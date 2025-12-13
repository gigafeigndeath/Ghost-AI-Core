from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.orchestrator import Orchestrator
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_llm

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: str
    platforms: list[str] = ["telegram", "vk", "business"]

@router.post("/generate_posts")
def generate_posts(request: AnalyzeRequest, db: Session = Depends(get_db), llm = Depends(get_llm)):
    try:
        orchestrator = Orchestrator(llm=llm, db=db)
        posts = orchestrator.process_article(request.url, request.platforms)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))