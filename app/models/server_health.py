from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.enums import ServerStatus, ServerType


class ServerHealth(Base):
    __tablename__ = "server_health"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    server_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("servers.id"),
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
