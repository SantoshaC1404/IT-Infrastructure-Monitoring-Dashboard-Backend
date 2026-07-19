from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.monitoring.collectors.collector_factory import CollectorFactory
from app.core.exceptions import SSHConnectionException
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.repositories.monitoring_snapshot_repository import (
    MonitoringSnapshotRepository,
)
from app.repositories.device_repository import DeviceRepository
from app.services.connection_service import ConnectionService
from app.utils.enums import DeviceStatus

logger = logging.getLogger(__name__)


class MonitoringService:

    def __init__(self, db: Session):

        self.db = db

        self.device_repository = DeviceRepository(db)

        self.snapshot_repository = MonitoringSnapshotRepository(db)

    # Monitor All Device
    def monitor_all_devices(self):

        devices = self.device_repository.get_monitoring_enabled()

        logger.info(
            "Starting monitoring for %d devices.",
            len(devices),
        )

        for device in devices:

            try:

                self.monitor_device(device.id)

            except Exception:

                logger.exception(
                    "Monitoring failed for device %s",
                    device.ip_address,
                )

    # Monitor Single Device
    def monitor_device(self, device_id: int):

        device = self.device_repository.get_by_id(device_id)

        if device is None:
            return

        try:

            with ConnectionService.connect(device) as ssh:

                # SQLAlchemy relationship
                inventory = device.inventory

                collector = CollectorFactory.get(
                    device_type=inventory.device_type,
                    ssh=ssh,
                )

                metrics = collector.collect()

            snapshot = MonitoringSnapshot(
                device_id=device.id,
                cpu_usage=metrics.cpu_usage,
                memory_usage=metrics.memory_usage,
                disk_usage=metrics.disk_usage,
                network_rx=metrics.network_rx,
                network_tx=metrics.network_tx,
                uptime=metrics.uptime,
                load_average=metrics.load_average,
                process_count=metrics.process_count,
            )

            self.snapshot_repository.create(
                snapshot,
                commit=False,
            )

            device.status = DeviceStatus.ONLINE

            device.last_seen = datetime.utcnow()

            self.db.commit()

            logger.info(
                "Monitoring completed for %s",
                device.ip_address,
            )

        except SSHConnectionException:

            self._mark_offline(device)

        except Exception:

            logger.exception(
                "Monitoring failed for %s",
                device.ip_address,
            )

            self._mark_offline(device)

    # Mark Device Offline
    def _mark_offline(self, device):

        device.status = DeviceStatus.OFFLINE

        self.db.commit()

        logger.warning(
            "%s marked OFFLINE.",
            device.ip_address,
        )
