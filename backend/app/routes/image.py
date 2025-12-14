# /var/www/Ghost-AI-Core/backend/app/routes/image.py
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.image_generator import generate_image

router = APIRouter()

class RegenerateRequest(BaseModel):
    platform: str
    prompt: str

@router.post("/regenerate_image")
def regenerate_image(request: RegenerateRequest):
    # Генерируем новую картинку по промпту поста
    new_image = generate_image(request.prompt)
    return {"image_url": new_image}
