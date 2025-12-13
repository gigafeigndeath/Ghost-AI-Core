from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.images import generate_image
from app.dependencies import get_image_gen

router = APIRouter()

class MediaRequest(BaseModel):
    prompt: str
    style: str = "default"

@router.post("/generate_image")
def generate_image_endpoint(request: MediaRequest, image_gen = Depends(get_image_gen)):
    try:
        image_url = generate_image(request.prompt, request.style)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))