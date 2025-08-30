from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.schemas import (
    AuthData,
    ProgressSummary,
    UserProgressResponse,
)
from app.core.services.game import game_service
from app.core.services.user import user_service
from app.db.base import get_db
from app.db.repositories.progress import progress_repository

router = APIRouter()


@router.get("/progress", response_model=list[UserProgressResponse])
async def get_user_progress(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    progress_list = progress_repository.get_user_progress(db, user.id)
    return progress_list


@router.get("/progress/summary", response_model=ProgressSummary)
async def get_progress_summary(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    summary = game_service.get_user_progress_summary(db, user.id)

    current_level = user_service.calculate_level(user.total_score)

    return ProgressSummary(
        total_score=summary["total_score"],
        total_completed=summary["total_completed"],
        total_attempts=summary["total_attempts"],
        completion_rate=summary["completion_rate"],
        average_score=summary["average_score"],
        current_level=current_level,
    )


@router.get("/progress/completed", response_model=list[UserProgressResponse])
async def get_completed_quests(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    completed = progress_repository.get_completed_quests(db, user.id)
    return completed
