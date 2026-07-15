from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.server_inventory import ServerInventory
from app.utils.enums import ServerStatus


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Friendly name shown in dashboard
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Connection Details
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

    # Monitoring
    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    status: Mapped[ServerStatus] = mapped_column(
        SQLEnum(ServerStatus),
        default=ServerStatus.UNKNOWN,
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships

    inventory = relationship(
        "ServerInventory",
        back_populates="server",
        uselist=False,
        cascade="all, delete-orphan",
    )

    snapshots = relationship(
        "MonitoringSnapshot",
        back_populates="server",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="server",
        cascade="all, delete-orphan",
    )

    network_interfaces = relationship(
        "NetworkInterface",
        back_populates="server",
        cascade="all, delete-orphan",
    )

    disks = relationship(
        "Disk",
        back_populates="server",
        cascade="all, delete-orphan",
    )
