from datetime import datetime
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class DeviceHealth(Base):
    __tablename__ = "device_health"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    device_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("devices.id"),
    )

    cpu_usage: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    memory_usage: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    disk_usage: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # status: Mapped[ServerStatus] = mapped_column(
    #     SQLEnum(ServerStatus),
    #     default=ServerStatus.UNKNOWN,
    # )

    # monitoring_enabled: Mapped[bool] = mapped_column(
    #     Boolean,
    #     default=True,
    # )

    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime,
    #     default=datetime.utcnow,
    # )
