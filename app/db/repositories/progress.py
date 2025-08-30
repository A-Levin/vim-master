from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import UserProgress
from app.db.repositories.base import BaseRepository


class ProgressRepository(BaseRepository[UserProgress, dict, dict]):
    def __init__(self):
        super().__init__(UserProgress)

    def get_user_progress(self, db: Session, user_id: int) -> list[UserProgress]:
        return db.query(UserProgress).filter(UserProgress.user_id == user_id).all()

    def get_quest_progress(
        self, db: Session, user_id: int, quest_id: int
    ) -> UserProgress | None:
        return (
            db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.quest_id == quest_id,
            )
            .first()
        )

    def get_completed_quests(self, db: Session, user_id: int) -> list[UserProgress]:
        return (
            db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.is_completed == True,
            )
            .all()
        )

    def create_or_update_progress(
        self,
        db: Session,
        user_id: int,
        quest_id: int,
        score: int = 0,
        is_completed: bool = False,
        hints_used: int = 0,
        time_spent: int | None = None,
    ) -> UserProgress:
        progress = self.get_quest_progress(db, user_id, quest_id)

        if progress:
            progress.attempts += 1
            progress.score = max(progress.score, score)
            progress.hints_used = max(progress.hints_used, hints_used)
            if is_completed and not progress.is_completed:
                progress.is_completed = True
                progress.completed_at = datetime.utcnow()
            if time_spent:
                progress.time_spent = time_spent
            progress.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(progress)
        else:
            progress_data = {
                "user_id": user_id,
                "quest_id": quest_id,
                "score": score,
                "attempts": 1,
                "hints_used": hints_used,
                "is_completed": is_completed,
                "time_spent": time_spent,
            }
            if is_completed:
                progress_data["completed_at"] = datetime.utcnow()

            progress = self.create(db, obj_in=progress_data)

        return progress


progress_repository = ProgressRepository()
