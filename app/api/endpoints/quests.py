from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.schemas import (
    AuthData,
    ChapterResponse,
    HintRequest,
    HintResponse,
    QuestResponse,
    QuestResult,
    QuestSubmission,
)
from app.core.services.game import game_service
from app.core.services.quest import quest_service
from app.db.base import get_db

router = APIRouter()


@router.get("/chapters", response_model=list[ChapterResponse])
async def get_chapters(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    chapters = quest_service.get_available_chapters(db)
    return chapters


@router.get("/chapters/{chapter_id}/quests", response_model=list[QuestResponse])
async def get_chapter_quests(
    chapter_id: int, auth_data: AuthData, db: Session = Depends(get_db)
):
    user = get_current_user(db, auth_data.init_data)
    quests = quest_service.get_chapter_quests(db, chapter_id)
    return quests


@router.get("/quests/{quest_id}", response_model=QuestResponse)
async def get_quest(quest_id: int, auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    quest = quest_service.get_quest_by_id(db, quest_id)

    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    return quest


@router.post("/quests/{quest_id}/start", response_model=QuestResponse)
async def start_quest(
    quest_id: int, auth_data: AuthData, db: Session = Depends(get_db)
):
    user = get_current_user(db, auth_data.init_data)
    quest = game_service.start_quest(db, user, quest_id)

    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    return quest


@router.post("/quests/submit", response_model=QuestResult)
async def submit_quest(
    submission: QuestSubmission, auth_data: AuthData, db: Session = Depends(get_db)
):
    user = get_current_user(db, auth_data.init_data)

    is_correct, score, message = game_service.submit_answer(
        db,
        user,
        submission.quest_id,
        submission.user_input,
        submission.time_spent,
        submission.hints_used,
    )

    next_quest_id = None
    if is_correct:
        next_quest = game_service.get_next_recommended_quest(db, user.id)
        if next_quest:
            next_quest_id = next_quest.id

    return QuestResult(
        is_correct=is_correct,
        score=score,
        message=message,
        next_quest_id=next_quest_id,
    )


@router.post("/quests/{quest_id}/hint", response_model=HintResponse)
async def get_quest_hint(
    quest_id: int,
    hint_request: HintRequest,
    auth_data: AuthData,
    db: Session = Depends(get_db),
):
    user = get_current_user(db, auth_data.init_data)
    quest = quest_service.get_quest_by_id(db, quest_id)

    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    hint = game_service.get_quest_hints(quest, hint_request.hints_used)
    hints_remaining = (
        len(quest.hints or []) - hint_request.hints_used - 1 if quest.hints else 0
    )

    return HintResponse(hint=hint, hints_remaining=max(0, hints_remaining))


@router.get("/quests/recommended", response_model=QuestResponse)
async def get_recommended_quest(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    quest = game_service.get_next_recommended_quest(db, user.id)

    if not quest:
        raise HTTPException(status_code=404, detail="No recommended quest found")

    return quest
