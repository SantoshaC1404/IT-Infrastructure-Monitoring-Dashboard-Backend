from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.utils.enums import DeviceType


class DeviceInventory(Base):
    __tablename__ = "device_inventories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    device_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # device_type: Mapped[DeviceType] = mapped_column(
    #     SQLEnum(DeviceType),
    #     nullable=False,
    # )
    device_type: Mapped[DeviceType] = mapped_column(
        SQLEnum(DeviceType),
        nullable=False,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
    )

    os_version: Mapped[str | None] = mapped_column(
        String(100),
    )

    kernel_version: Mapped[str | None] = mapped_column(
        String(100),
    )

    architecture: Mapped[str | None] = mapped_column(
        String(50),
    )

    cpu_model: Mapped[str | None] = mapped_column(
        String(255),
    )

    # cpu_cores: Mapped[int | None]

    # logical_processors: Mapped[int | None]

    cpu_vendor: Mapped[str | None] = mapped_column(
        String(100),
    )

    cpu_architecture: Mapped[str | None] = mapped_column(
        String(100),
    )

    physical_cores: Mapped[int | None] = mapped_column(
        Integer,
    )

    # total_memory: Mapped[int | None]
    # total_memory_bytes: Mapped[int | None]
    available_memory_bytes: Mapped[int | None] = mapped_column(
        Integer,
    )

    used_memory_bytes: Mapped[int | None] = mapped_column(
        Integer,
    )

    # total_disk: Mapped[int | None]
    total_disk_bytes: Mapped[int | None] = mapped_column(
        Integer,
    )

    # mac_address: Mapped[str | None] = mapped_column(
    #     String(50),
    # )

    virtualization: Mapped[str | None] = mapped_column(
        String(100),
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    device = relationship(
        "Device",
        back_populates="inventory",
    )

    logical_cores: Mapped[int | None] = mapped_column(Integer)

    total_memory_bytes: Mapped[int | None] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
