from fastapi import APIRouter

from app.api.endpoints import auth, progress, quests

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
