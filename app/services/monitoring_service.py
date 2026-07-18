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
from app.repositories.server_repository import ServerRepository
from app.services.connection_service import ConnectionService
from app.utils.enums import ServerStatus

logger = logging.getLogger(__name__)


class MonitoringService:

    def __init__(self, db: Session):

        self.db = db

        self.server_repository = ServerRepository(db)

        self.snapshot_repository = MonitoringSnapshotRepository(db)

    # ==========================================================
    # Monitor All Servers
    # ==========================================================

    def monitor_all_servers(self):

        servers = self.server_repository.get_monitoring_enabled()

        logger.info(
            "Starting monitoring for %d servers.",
            len(servers),
        )

        for server in servers:

            try:

                self.monitor_server(server.id)

            except Exception:

                logger.exception(
                    "Monitoring failed for server %s",
                    server.ip_address,
                )

    # ==========================================================
    # Monitor Single Server
    # ==========================================================

    def monitor_server(self, server_id: int):

        server = self.server_repository.get_by_id(server_id)

        if server is None:
            return

        try:

            with ConnectionService.connect(server) as ssh:

                # SQLAlchemy relationship
                inventory = server.inventory

                # One-to-Many safety
                # if isinstance(inventory, list):

                #     if not inventory:
                #         raise Exception("Inventory not found.")

                #     inventory = inventory[0]

                collector = CollectorFactory.get(
                    server_type=inventory.server_type,
                    ssh=ssh,
                )

                metrics = collector.collect()

            snapshot = MonitoringSnapshot(
                server_id=server.id,
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

            server.status = ServerStatus.ONLINE

            server.last_seen = datetime.utcnow()

            self.db.commit()

            logger.info(
                "Monitoring completed for %s",
                server.ip_address,
            )

        except SSHConnectionException:

            self._mark_offline(server)

        except Exception:

            logger.exception(
                "Monitoring failed for %s",
                server.ip_address,
            )

            self._mark_offline(server)

    # ==========================================================
    # Mark Server Offline
    # ==========================================================

    def _mark_offline(self, server):

        server.status = ServerStatus.OFFLINE

        self.db.commit()

        logger.warning(
            "%s marked OFFLINE.",
            server.ip_address,
        )
