from datetime import datetime, timedelta

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.monitoring_snapshot import MonitoringSnapshot


class MonitoringSnapshotRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, snapshot: MonitoringSnapshot) -> MonitoringSnapshot:
        self.db.add(snapshot)
        # self.db.commit()
        # self.db.refresh(snapshot)
        return snapshot

    def bulk_create(
        self,
        snapshots: list[MonitoringSnapshot],
    ) -> None:
        self.db.add_all(snapshots)
        self.db.commit()

    def latest(
        self,
        server_id: int,
    ) -> MonitoringSnapshot | None:

        stmt = (
            select(MonitoringSnapshot)
            .where(MonitoringSnapshot.server_id == server_id)
            .order_by(desc(MonitoringSnapshot.collected_at))
            .limit(1)
        )

        return self.db.scalar(stmt)

    def history(
        self,
        server_id: int,
        hours: int = 24,
    ) -> list[MonitoringSnapshot]:

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = (
            select(MonitoringSnapshot)
            .where(
                MonitoringSnapshot.server_id == server_id,
                MonitoringSnapshot.collected_at >= since,
            )
            .order_by(MonitoringSnapshot.collected_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def latest_for_all_servers(self):

        subquery = (
            select(
                MonitoringSnapshot.server_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.server_id)
            .subquery()
        )

        stmt = select(MonitoringSnapshot).join(
            subquery,
            (MonitoringSnapshot.server_id == subquery.c.server_id)
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
        server_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.cpu_usage)).where(
            MonitoringSnapshot.server_id == server_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)

    def average_memory(
        self,
        server_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.memory_usage)).where(
            MonitoringSnapshot.server_id == server_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)

    def average_disk(
        self,
        server_id: int,
        hours: int = 24,
    ):

        since = datetime.utcnow() - timedelta(hours=hours)

        stmt = select(func.avg(MonitoringSnapshot.disk_usage)).where(
            MonitoringSnapshot.server_id == server_id,
            MonitoringSnapshot.collected_at >= since,
        )

        return self.db.scalar(stmt)
