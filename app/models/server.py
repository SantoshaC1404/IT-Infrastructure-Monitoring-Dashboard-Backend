from sqlalchemy import DateTime, Integer, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.utils.enums import ServerType, ServerStatus


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    ssh_port: Mapped[int] = mapped_column(
        Integer,
        default=22,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    encrypted_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    server_type: Mapped[ServerType] = mapped_column(
        SQLEnum(ServerType),
    )

    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    status: Mapped[ServerStatus] = mapped_column(
        SQLEnum(ServerStatus),
        default=ServerStatus.UNKNOWN,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    snapshots: Mapped[list["MonitoringSnapshot"]] = relationship(
        back_populates="server",
        cascade="all, delete-orphan",
    )
