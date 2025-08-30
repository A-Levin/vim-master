import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl, unquote

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.core.services.user import user_service

settings = get_settings()


def validate_telegram_auth(init_data: str) -> dict:
    try:
        parsed_data = dict(parse_qsl(init_data))

        auth_date = parsed_data.get("auth_date")
        if not auth_date:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth_date"
            )

        auth_timestamp = int(auth_date)
        current_timestamp = int(time.time())

        if current_timestamp - auth_timestamp > 86400:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth data expired"
            )

        received_hash = parsed_data.pop("hash", "")

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items())
        )

        secret_key = hmac.new(
            b"WebAppData", settings.telegram_bot_token.encode(), hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(received_hash, calculated_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid hash"
            )

        user_data = json.loads(unquote(parsed_data.get("user", "{}")))

        return {
            "user_id": user_data.get("id"),
            "username": user_data.get("username"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "language_code": user_data.get("language_code", "en"),
        }

    except (ValueError, KeyError, json.JSONDecodeError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid auth data: {e!s}"
        )


def get_current_user(db: Session, init_data: str):
    auth_data = validate_telegram_auth(init_data)

    user = user_service.get_or_create_user(
        db,
        telegram_id=auth_data["user_id"],
        username=auth_data["username"],
        first_name=auth_data["first_name"],
        last_name=auth_data.get("last_name"),
    )

    return user
