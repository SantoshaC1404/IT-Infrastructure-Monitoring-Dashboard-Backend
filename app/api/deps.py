from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions.auth import (
    InactiveUserException,
    InsufficientPermissionsException,
    InvalidTokenException,
)
from app.core.security.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.utils.enums import UserRole

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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None or "jti" not in payload:
        raise InvalidTokenException()

    if TokenRepository(db).is_revoked(payload["jti"]):
        raise InvalidTokenException("This session has been logged out.")

    user = UserRepository(db).get_by_username(payload["sub"])

    if user is None:
        raise InvalidTokenException()

    if not user.is_active:
        raise InactiveUserException()

    return user


def require_role(*allowed_roles: UserRole):
    """
    Dependency factory for role-based access control.

    Usage:
        @router.get("/admin-only", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """

    def _check_role(current_user: User = Depends(get_current_user)) -> User:

        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsException()

        return current_user

    return _check_role
