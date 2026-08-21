from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.revoked_token import RevokedToken


class TokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def revoke(self, jti: str, expires_at: datetime) -> RevokedToken:
        revoked = RevokedToken(
            jti=jti,
            expires_at=expires_at,
        )

        self.db.add(revoked)
        self.db.commit()
        self.db.refresh(revoked)

        return revoked

    def is_revoked(self, jti: str) -> bool:
        return (
            self.db.query(RevokedToken)
            .filter(RevokedToken.jti == jti)
            .first()
            is not None
        )

    def purge_expired(self) -> int:
        """
        Housekeeping: delete blacklist entries whose underlying token has
        already expired naturally (they no longer need to be tracked).
        Call this from a periodic job if you add one.
        """

        deleted = (
            self.db.query(RevokedToken)
            .filter(RevokedToken.expires_at < datetime.now(timezone.utc))
            .delete()
        )

        self.db.commit()

        return deleted
