import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import LoginRequest, TokenResponse
from app.service.user.login import login_user


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=TokenResponse, summary="Authenticate user")
def login(request: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    logger.info("Login attempt", extra={"username": request.username})
    try:
        token = login_user(db=db, username=request.username, password=request.password)
    except ValueError as error:
        logger.warning(
            "Login failed",
            extra={"username": request.username, "reason": str(error)},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error

    logger.info("Login succeeded", extra={"user_id": request.username})
    return TokenResponse(access_token=token)


