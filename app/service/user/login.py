from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.repository.user.getUserByUsername import get_user_by_username


def login_user(db: Session, username: str, password: str) -> str:
    user = get_user_by_username(db, username)
    if user is None:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    settings = get_settings()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    return create_access_token(subject=str(user.id), expires_delta=expires_delta)


