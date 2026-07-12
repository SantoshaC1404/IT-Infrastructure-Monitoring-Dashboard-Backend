from sqlalchemy.orm import Session

from app.models.monitoring_snapshot import MonitoringSnapshot


class MonitoringRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_snapshot(self, snapshot):

        self.db.add(snapshot)

        self.db.commit()

        self.db.refresh(snapshot)

        return snapshot

    def latest(self, server_id: int):

        return (
            self.db.query(MonitoringSnapshot)
            .filter(MonitoringSnapshot.server_id == server_id)
            .order_by(MonitoringSnapshot.collected_at.desc())
            .first()
        )
