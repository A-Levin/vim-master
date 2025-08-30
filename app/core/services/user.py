from sqlalchemy.orm import Session

from app.db.models import User
from app.db.repositories.user import user_repository


class UserService:
    def __init__(self):
        self.repository = user_repository

    def get_or_create_user(
        self,
        db: Session,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None = None,
    ) -> User:
        user = self.repository.get_by_telegram_id(db, telegram_id)

        if not user:
            user = self.repository.create_from_telegram(
                db, telegram_id, username, first_name, last_name
            )
        else:
            if user.username != username or user.first_name != first_name:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                db.commit()
                db.refresh(user)

            self.repository.update_last_activity(db, user.id)

        return user

    def update_user_score(self, db: Session, user_id: int, score: int) -> User | None:
        return self.repository.add_score(db, user_id, score)

    def get_user_by_telegram_id(self, db: Session, telegram_id: int) -> User | None:
        return self.repository.get_by_telegram_id(db, telegram_id)

    def calculate_level(self, total_score: int) -> int:
        if total_score < 50:
            return 1
        elif total_score < 150:
            return 2
        elif total_score < 300:
            return 3
        elif total_score < 500:
            return 4
        elif total_score < 750:
            return 5
        else:
            return min(10, 5 + (total_score - 750) // 250)


user_service = UserService()
