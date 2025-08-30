from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.schemas import AuthData, UserResponse
from app.db.base import get_db

router = APIRouter()


@router.post("/login", response_model=UserResponse)
async def login(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(auth_data: AuthData, db: Session = Depends(get_db)):
    user = get_current_user(db, auth_data.init_data)
    return user
