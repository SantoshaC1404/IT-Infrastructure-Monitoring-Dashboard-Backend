from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions.auth import InvalidTokenException
from app.core.security.security import decode_access_token
from app.repositories.token_repository import TokenRepository


class LogoutService:

    def __init__(self, db: Session):
        self.token_repo = TokenRepository(db)

    def logout(self, token: str) -> None:
        """
        Revokes the given access token so it can no longer be used, even
        though it hasn't naturally expired yet.
        """

        payload = decode_access_token(token)

        if payload is None or "jti" not in payload:
            raise InvalidTokenException()

        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        if self.token_repo.is_revoked(payload["jti"]):
            return  # already logged out - treat as a no-op, not an error

        self.token_repo.revoke(payload["jti"], expires_at)
