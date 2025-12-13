from fastapi import APIRouter

router = APIRouter()

@router.get("/check")
def health_check():
    return {"status": "healthy", "message": "Ghost AI is ready to extend news life! Конкурс МПИТ."}