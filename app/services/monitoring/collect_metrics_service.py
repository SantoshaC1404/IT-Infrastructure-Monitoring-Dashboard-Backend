from datetime import datetime

from sqlalchemy.orm import Session

from app.connectors.connector_factory import ConnectorFactory
from app.core.encryption import encryption_service
from app.core.exceptions import ConnectionException
from app.monitoring.collectors.collector_factory import CollectorFactory
from app.repositories.device_repository import DeviceRepository
from app.services.monitoring.save_snapshot_service import (
    SaveSnapshotService,
)
from app.services.monitoring.monitoring_device_service import (
    MonitoringDeviceService,
)
from app.core.logger import logger


class CollectMetricsService:

    def __init__(self, db: Session):

        self.db = db

        self.device_repository = DeviceRepository(db)

        self.snapshot_service = SaveSnapshotService(db)

        self.device_service = MonitoringDeviceService(db)

    # -----------------------------------------------------

    def monitor_all_devices(self):

        devices = self.device_repository.get_monitoring_enabled()

        for device in devices:

            try:

                self.monitor_device(device.id)

            except Exception:

                logger.exception(
                    "Monitoring failed for %s",
                    device.ip_address,
                )

    # -----------------------------------------------------

    def monitor_device(
        self,
        device_id: int,
    ):

        device = self.device_repository.get_by_id(device_id)

        if device is None:
            return

        connector = ConnectorFactory.create(
            device=device,
            password=encryption_service.decrypt(device.encrypted_password),
        )

        try:

            with connector:

                collector = CollectorFactory.create(
                    device.device_type,
                    connector,
                )

                metrics = collector.collect()

            self.snapshot_service.save_snapshot(
                device.id,
                metrics,
            )

            self.device_service.mark_online(
                device,
            )

        except ConnectionException:

            self.device_service.mark_offline(
                device,
            )
