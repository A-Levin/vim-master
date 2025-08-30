from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models import DifficultyLevel, QuestType, UserStatus


class UserBase(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    language_code: str = "en"


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    status: UserStatus
    total_score: int
    current_level: int
    created_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True


class ChapterResponse(BaseModel):
    id: int
    title: str
    description: str | None
    difficulty: DifficultyLevel
    order_index: int
    unlock_score: int

    class Config:
        from_attributes = True


class QuestResponse(BaseModel):
    id: int
    chapter_id: int
    title: str
    description: str
    quest_type: QuestType
    difficulty: DifficultyLevel
    order_index: int
    initial_text: str | None
    expected_result: str | None
    max_score: int
    time_limit: int | None

    class Config:
        from_attributes = True


class QuestSubmission(BaseModel):
    quest_id: int
    user_input: str
    time_spent: int | None = None
    hints_used: int = 0


class QuestResult(BaseModel):
    is_correct: bool
    score: int
    message: str
    next_quest_id: int | None = None


class UserProgressResponse(BaseModel):
    id: int
    quest_id: int
    is_completed: bool
    score: int
    attempts: int
    hints_used: int
    time_spent: int | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    total_score: int
    total_completed: int
    total_attempts: int
    completion_rate: float
    average_score: float
    current_level: int


class HintRequest(BaseModel):
    quest_id: int
    hints_used: int


class HintResponse(BaseModel):
    hint: str | None
    hints_remaining: int


class AuthData(BaseModel):
    init_data: str = Field(..., description="Telegram Web App init data")
