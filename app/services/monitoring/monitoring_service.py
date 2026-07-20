from sqlalchemy.orm import Session

from app.services.monitoring.collect_metrics_service import (
    CollectMetricsService,
)
from app.services.monitoring.save_snapshot_service import (
    SaveSnapshotService,
)
from app.services.monitoring.monitoring_device_service import (
    MonitoringDeviceService,
)


class MonitoringService:

    def __init__(self, db: Session):

        self.collect_service = CollectMetricsService(db)
        self.snapshot_service = SaveSnapshotService(db)
        self.device_service = MonitoringDeviceService(db)

    def monitor_all_devices(self):

        self.collect_service.monitor_all_devices()

    def monitor_device(
        self,
        device_id: int,
    ):

        self.collect_service.monitor_device(device_id)
