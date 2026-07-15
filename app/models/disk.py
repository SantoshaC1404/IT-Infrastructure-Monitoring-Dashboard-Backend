from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.server import Server


class Disk(Base):
    __tablename__ = "disks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    server_id: Mapped[int] = mapped_column(
        ForeignKey("servers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    device_name: Mapped[str] = mapped_column(
        String(100),
    )

    mount_point: Mapped[str] = mapped_column(
        String(255),
    )

    filesystem: Mapped[str] = mapped_column(
        String(50),
    )

    total_bytes: Mapped[int] = mapped_column(
        BigInteger,
    )

    used_bytes: Mapped[int] = mapped_column(
        BigInteger,
    )

    free_bytes: Mapped[int] = mapped_column(
        BigInteger,
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
        back_populates="disks",
    )
