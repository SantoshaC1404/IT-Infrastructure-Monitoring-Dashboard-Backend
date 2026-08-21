from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions.auth import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.core.security.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class LoginService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def login(self, username: str, password: str) -> tuple[str, int]:
        """
        Returns (access_token, expires_in_seconds).
        """

        user = self.user_repo.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        token, _jti, expires_at = create_access_token(subject=user.username)

        expires_in = int(
            (expires_at - datetime.now(timezone.utc)).total_seconds()
        )

        return token, expires_in
