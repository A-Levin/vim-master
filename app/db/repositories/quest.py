from sqlalchemy.orm import Session

from app.db.models import Chapter, DifficultyLevel, Quest, QuestType
from app.db.repositories.base import BaseRepository


class QuestRepository(BaseRepository[Quest, dict, dict]):
    def __init__(self):
        super().__init__(Quest)

    def get_by_chapter(self, db: Session, chapter_id: int) -> list[Quest]:
        return (
            db.query(Quest)
            .filter(Quest.chapter_id == chapter_id, Quest.is_active == True)
            .order_by(Quest.order_index)
            .all()
        )

    def get_by_type(self, db: Session, quest_type: QuestType) -> list[Quest]:
        return (
            db.query(Quest)
            .filter(Quest.quest_type == quest_type, Quest.is_active == True)
            .all()
        )

    def get_by_difficulty(
        self, db: Session, difficulty: DifficultyLevel
    ) -> list[Quest]:
        return (
            db.query(Quest)
            .filter(Quest.difficulty == difficulty, Quest.is_active == True)
            .all()
        )


class ChapterRepository(BaseRepository[Chapter, dict, dict]):
    def __init__(self):
        super().__init__(Chapter)

    def get_active_chapters(self, db: Session) -> list[Chapter]:
        return (
            db.query(Chapter)
            .filter(Chapter.is_active == True)
            .order_by(Chapter.order_index)
            .all()
        )

    def get_by_difficulty(
        self, db: Session, difficulty: DifficultyLevel
    ) -> list[Chapter]:
        return (
            db.query(Chapter)
            .filter(Chapter.difficulty == difficulty, Chapter.is_active == True)
            .order_by(Chapter.order_index)
            .all()
        )


quest_repository = QuestRepository()
chapter_repository = ChapterRepository()
