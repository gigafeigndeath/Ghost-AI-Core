from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.posting import post_to_platform
from app.dependencies import get_poster

router = APIRouter()

class PublishRequest(BaseModel):
    platform: str
    content: str
    image_url: str = None
    schedule_time: str = None  # ISO format

@router.post("/post")
def publish_post(request: PublishRequest, poster = Depends(get_poster)):
    try:
        result = post_to_platform(request.platform, request.content, request.image_url, request.schedule_time)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))