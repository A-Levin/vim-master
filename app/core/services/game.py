from typing import Any

from sqlalchemy.orm import Session

from app.core.services.quest import quest_service
from app.core.services.user import user_service
from app.db.models import Quest, User
from app.db.repositories.progress import progress_repository


class GameService:
    def __init__(self):
        self.progress_repository = progress_repository
        self.user_service = user_service
        self.quest_service = quest_service

    def start_quest(self, db: Session, user: User, quest_id: int) -> Quest | None:
        quest = self.quest_service.get_quest_by_id(db, quest_id)
        if not quest:
            return None

        progress = self.progress_repository.get_quest_progress(db, user.id, quest_id)
        if not progress:
            self.progress_repository.create_or_update_progress(
                db, user.id, quest_id, score=0, is_completed=False
            )

        return quest

    def submit_answer(
        self,
        db: Session,
        user: User,
        quest_id: int,
        user_input: str,
        time_spent: int | None = None,
        hints_used: int = 0,
    ) -> tuple[bool, int, str]:
        quest = self.quest_service.get_quest_by_id(db, quest_id)
        if not quest:
            return False, 0, "Quest not found"

        progress = self.progress_repository.get_quest_progress(db, user.id, quest_id)
        if not progress:
            return False, 0, "Quest not started"

        if progress.is_completed:
            return False, 0, "Quest already completed"

        is_correct = self.quest_service.validate_vim_command(
            user_input, quest.vim_command or ""
        )

        attempts = progress.attempts + 1

        score = self.quest_service.calculate_quest_score(
            quest, is_correct, attempts, hints_used, time_spent
        )

        self.progress_repository.create_or_update_progress(
            db,
            user.id,
            quest_id,
            score=score,
            is_completed=is_correct,
            hints_used=hints_used,
            time_spent=time_spent,
        )

        if is_correct:
            self.user_service.update_user_score(db, user.id, score)
            message = f"Correct! You earned {score} points."
        else:
            message = "Incorrect. Try again!"

        return is_correct, score, message

    def get_user_progress_summary(self, db: Session, user_id: int) -> dict[str, Any]:
        progress_list = self.progress_repository.get_user_progress(db, user_id)
        completed_quests = [p for p in progress_list if p.is_completed]

        total_score = sum(p.score for p in completed_quests)
        total_completed = len(completed_quests)
        total_attempts = sum(p.attempts for p in progress_list)

        return {
            "total_score": total_score,
            "total_completed": total_completed,
            "total_attempts": total_attempts,
            "completion_rate": (
                total_completed / len(progress_list) if progress_list else 0
            ),
            "average_score": (
                total_score / total_completed if total_completed > 0 else 0
            ),
        }

    def get_next_recommended_quest(self, db: Session, user_id: int) -> Quest | None:
        completed_progress = self.progress_repository.get_completed_quests(db, user_id)
        completed_quest_ids = {p.quest_id for p in completed_progress}

        beginner_quests = self.quest_service.get_beginner_quests(db)

        for quest in beginner_quests:
            if quest.id not in completed_quest_ids:
                return quest

        return None

    def get_quest_hints(self, quest: Quest, hints_used: int) -> str | None:
        if not quest.hints or hints_used >= len(quest.hints):
            return None

        return quest.hints[hints_used]


game_service = GameService()
