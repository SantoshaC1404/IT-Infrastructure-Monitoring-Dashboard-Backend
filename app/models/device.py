from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.utils.enums import DeviceType, DeviceStatus


class Device(Base):
    __tablename__ = "devices"

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

    device_type: Mapped[DeviceType] = mapped_column(
        SQLEnum(DeviceType),
        nullable=False,
    )

    # Monitoring
    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    status: Mapped[DeviceStatus] = mapped_column(
        SQLEnum(DeviceStatus),
        default=DeviceStatus.UNKNOWN,
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
        "DeviceInventory",
        back_populates="device",
        uselist=False,
        cascade="all, delete-orphan",
    )

    snapshots = relationship(
        "MonitoringSnapshot",
        back_populates="device",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="device",
        cascade="all, delete-orphan",
    )

    network_interfaces = relationship(
        "NetworkInterface",
        back_populates="device",
        cascade="all, delete-orphan",
    )

    disks = relationship(
        "Disk",
        back_populates="device",
        cascade="all, delete-orphan",
    )
