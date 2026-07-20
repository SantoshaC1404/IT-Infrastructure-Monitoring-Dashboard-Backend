from sqlalchemy.orm import Session

from app.models.monitoring_snapshot import MonitoringSnapshot
from app.repositories.monitoring_snapshot_repository import (
    MonitoringSnapshotRepository,
)


class SaveSnapshotService:

    def __init__(self, db: Session):

        self.repository = MonitoringSnapshotRepository(db)

    def save_snapshot(
        self,
        device_id: int,
        metrics,
    ):

        snapshot = MonitoringSnapshot(
            device_id=device_id,
            cpu_usage=metrics.cpu_usage,
            memory_usage=metrics.memory_usage,
            disk_usage=metrics.disk_usage,
            network_rx=metrics.network_rx,
            network_tx=metrics.network_tx,
            # uptime=metrics.uptime,
            load_average=metrics.load_average,
            # process_count=metrics.process_count,
        )

        self.repository.create(
            snapshot,
            commit=False,
        )
