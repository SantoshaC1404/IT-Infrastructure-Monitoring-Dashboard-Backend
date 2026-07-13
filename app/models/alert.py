from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.enums import AlertSeverity, AlertStatus


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    server_id: Mapped[int] = mapped_column(
        ForeignKey("servers.id", ondelete="CASCADE"),
        index=True,
    )

    severity: Mapped[AlertSeverity] = mapped_column(SQLEnum(AlertSeverity))

    title: Mapped[str] = mapped_column(String(200))

    message: Mapped[str] = mapped_column(String(500))

    metric: Mapped[str] = mapped_column(String(50))

    metric_value: Mapped[float] = mapped_column(Float)

    threshold: Mapped[float] = mapped_column(Float)

    status: Mapped[AlertStatus] = mapped_column(
        SQLEnum(AlertStatus),
        default=AlertStatus.OPEN,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
