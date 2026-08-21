from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class RevokedToken(Base):
    """
    Tracks JWTs that have been explicitly logged out before their natural
    expiry. JWTs are stateless by design, so "logout" for a bearer token
    means recording its unique id (jti) here and rejecting it on every
    subsequent request until it would have expired anyway.
    """

    __tablename__ = "revoked_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    jti: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
