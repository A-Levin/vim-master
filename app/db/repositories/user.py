from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import User
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, dict, dict]):
    def __init__(self):
        super().__init__(User)

    def get_by_telegram_id(self, db: Session, telegram_id: int) -> User | None:
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def create_from_telegram(
        self,
        db: Session,
        telegram_id: int,
        username: str,
        first_name: str,
        last_name: str | None = None,
    ) -> User:
        user_data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
        return self.create(db, obj_in=user_data)

    def update_last_activity(self, db: Session, user_id: int) -> User | None:
        user = self.get(db, user_id)
        if user:
            user.last_activity = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user

    def add_score(self, db: Session, user_id: int, score: int) -> User | None:
        user = self.get(db, user_id)
        if user:
            user.total_score += score
            db.commit()
            db.refresh(user)
        return user


user_repository = UserRepository()
