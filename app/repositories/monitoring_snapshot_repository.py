from datetime import datetime, timedelta

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.monitoring_snapshot import MonitoringSnapshot


class MonitoringSnapshotRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        snapshot: MonitoringSnapshot,
        commit: bool = True,
    ) -> MonitoringSnapshot:

        self.db.add(snapshot)

        if commit:
            self.db.commit()
            self.db.flush(snapshot)

        return snapshot

    def bulk_create(
        self,
        snapshots: list[MonitoringSnapshot],
    ) -> None:
        self.db.add_all(snapshots)
        self.db.commit()

    def latest(
        self,
        device_id: int,
    ) -> MonitoringSnapshot | None:

        stmt = (
            select(MonitoringSnapshot)
            .where(MonitoringSnapshot.device_id == device_id)
            .order_by(desc(MonitoringSnapshot.collected_at))
            .limit(1)
        )

        return self.db.scalar(stmt)

    def history(
        self,
        device_id: int,
        hours: int = 24,
    ) -> list[MonitoringSnapshot]:

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = (
            select(MonitoringSnapshot)
            .where(
                MonitoringSnapshot.device_id == device_id,
                MonitoringSnapshot.collected_at >= since,
            )
            .order_by(MonitoringSnapshot.collected_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def latest_for_all_devices(self):

        subquery = (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

        stmt = select(MonitoringSnapshot).join(
            subquery,
            (MonitoringSnapshot.device_id == subquery.c.device_id)
            & (MonitoringSnapshot.collected_at == subquery.c.latest),
        )

        return list(self.db.scalars(stmt).all())

    def delete_old_snapshots(
        self,
        retention_days: int,
    ):

        cutoff = datetime.utcnow() - timedelta(days=retention_days)

        self.db.query(MonitoringSnapshot).filter(
            MonitoringSnapshot.collected_at < cutoff
        ).delete()

        self.db.commit()

    def average_cpu(
        self,
        device_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.cpu_usage)).where(
            MonitoringSnapshot.device_id == device_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)

    def average_memory(
        self,
        device_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.memory_usage)).where(
            MonitoringSnapshot.device_id == device_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)

    def average_disk(
        self,
        device_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.disk_usage)).where(
            MonitoringSnapshot.device_id == device_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)
