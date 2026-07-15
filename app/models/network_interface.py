from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.server import Server


class NetworkInterface(Base):
    __tablename__ = "network_interfaces"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    server_id: Mapped[int] = mapped_column(
        ForeignKey("servers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    interface_name: Mapped[str] = mapped_column(
        String(100),
    )

    mac_address: Mapped[str | None] = mapped_column(
        String(50),
    )

    ipv4_address: Mapped[str | None] = mapped_column(
        String(50),
    )

    ipv6_address: Mapped[str | None] = mapped_column(
        String(100),
    )

    speed_mbps: Mapped[int | None]

    is_up: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    server: Mapped["Server"] = relationship(
        "Server",
        back_populates="network_interfaces",
    )
