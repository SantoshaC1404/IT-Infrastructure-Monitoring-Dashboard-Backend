from fastapi import FastAPI, status, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from collections.abc import Generator
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import SessionLocal
from app.core.security.security import decode_access_token
from app.repositories.user_repository import UserRepository

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.
    This function is used as a dependency in FastAPI routes to provide a database session.
    It yields a session and ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token=token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    username = payload.get("sub")

    repo = UserRepository(db)

    user = repo.get_user_by_name(username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user
"""


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(401, "Invalid token")

    username = payload["sub"]

    repo = UserRepository(db)

    user = repo.get_by_username(username)

    if user is None:
        raise HTTPException(401, "User not found")

    return user
