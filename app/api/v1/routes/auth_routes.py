from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, security
from app.models.user import User
from app.schemas.auth.token import LoginRequest, TokenResponse
from app.schemas.auth.user import UserCreate, UserResponse
from app.schemas.common import MessageResponse
from app.services.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register(user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    access_token, expires_in = AuthService(db).login(
        login_request.username,
        login_request.password,
    )

    return TokenResponse(
        access_token=access_token,
        expires_in=expires_in,
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    # Ensures the caller is currently authenticated before letting them
    # log themselves out.
    _current_user: User = Depends(get_current_user),
):
    AuthService(db).logout(credentials.credentials)

    return MessageResponse(message="Logged out successfully.")


@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(user: User = Depends(get_current_user)):
    return user
