from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.utils.enums import AlertSeverity, AlertStatus


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # event id
    event_id = mapped_column(
        ForeignKey("events.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    severity: Mapped[AlertSeverity] = mapped_column(
        SQLEnum(AlertSeverity),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    metric: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    metric_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[AlertStatus] = mapped_column(
        SQLEnum(AlertStatus),
        default=AlertStatus.OPEN,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    device = relationship(
        "Device",
        back_populates="alerts",
    )
