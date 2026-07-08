from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.schemas.auth import Token, LoginRequest
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_date: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)

    try:
        user = auth_service.register(user_date)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token = auth_service.login(login_request.username, login_request.password)

    print(token)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def current_user(user: User = Depends(get_current_user)):
    return user
