from sqlalchemy.orm import Session

from app.db.models import Chapter, DifficultyLevel, Quest
from app.db.repositories.quest import chapter_repository, quest_repository


class QuestService:
    def __init__(self):
        self.quest_repository = quest_repository
        self.chapter_repository = chapter_repository

    def get_available_chapters(self, db: Session) -> list[Chapter]:
        return self.chapter_repository.get_active_chapters(db)

    def get_chapter_quests(self, db: Session, chapter_id: int) -> list[Quest]:
        return self.quest_repository.get_by_chapter(db, chapter_id)

    def get_quest_by_id(self, db: Session, quest_id: int) -> Quest | None:
        return self.quest_repository.get(db, quest_id)

    def get_beginner_quests(self, db: Session) -> list[Quest]:
        return self.quest_repository.get_by_difficulty(db, DifficultyLevel.BEGINNER)

    def get_next_quest_in_chapter(
        self, db: Session, chapter_id: int, current_order: int
    ) -> Quest | None:
        quests = self.get_chapter_quests(db, chapter_id)
        for quest in quests:
            if quest.order_index > current_order:
                return quest
        return None

    def validate_vim_command(self, user_input: str, expected_command: str) -> bool:
        user_input = user_input.strip()
        expected_command = expected_command.strip()

        if user_input == expected_command:
            return True

        normalized_input = self._normalize_vim_command(user_input)
        normalized_expected = self._normalize_vim_command(expected_command)

        return normalized_input == normalized_expected

    def _normalize_vim_command(self, command: str) -> str:
        command = command.strip()

        aliases = {
            "substitute": "s",
            "global": "g",
            "write": "w",
            "quit": "q",
        }

        for full, short in aliases.items():
            command = command.replace(full, short)

        return command

    def calculate_quest_score(
        self,
        quest: Quest,
        is_correct: bool,
        attempts: int,
        hints_used: int,
        time_spent: int | None = None,
    ) -> int:
        if not is_correct:
            return 0

        base_score = quest.max_score

        score = base_score

        if attempts > 1:
            penalty = min(0.2 * (attempts - 1), 0.5)
            score = int(score * (1 - penalty))

        if hints_used > 0:
            hint_penalty = min(0.1 * hints_used, 0.3)
            score = int(score * (1 - hint_penalty))

        if quest.time_limit and time_spent and time_spent > quest.time_limit:
            time_penalty = min(
                0.1 * ((time_spent - quest.time_limit) / quest.time_limit), 0.2
            )
            score = int(score * (1 - time_penalty))

        return max(1, score) if is_correct else 0


quest_service = QuestService()
