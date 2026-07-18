from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.utils.enums import DeviceType


class ServerInventory(Base):
    __tablename__ = "server_inventories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    server_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("servers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    server_type: Mapped[DeviceType] = mapped_column(
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
    cpu_vendor: Mapped[int | None]

    cpu_model: Mapped[str | None]

    cpu_architecture: Mapped[str | None]

    physical_cores: Mapped[int | None]

    # logical_cores: Mapped[int | None]

    # total_memory: Mapped[int | None]
    # total_memory_bytes: Mapped[int | None]
    available_memory_bytes: Mapped[int | None]

    used_memory_bytes: Mapped[int | None]

    # total_disk: Mapped[int | None]
    total_disk_bytes: Mapped[int | None]

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

    server = relationship(
        "Server",
        back_populates="inventory",
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
