from fastapi import FastAPI
from .routes.api import router as api_router

app = FastAPI(title="PR AI Agent Backend")

app.include_router(api_router, prefix="/api")
