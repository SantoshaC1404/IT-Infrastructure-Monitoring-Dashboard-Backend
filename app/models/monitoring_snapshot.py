from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class MonitoringSnapshot(Base):

    __tablename__ = "monitoring_snapshots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"),
        index=True,
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

    load_average: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    network_rx: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
    )

    network_tx: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
    )

    uptime_seconds: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    device = relationship(
        "Device",
        back_populates="snapshots",
    )
