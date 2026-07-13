from app.collectors.factory import CollectorFactory
from app.core.encryption import encryption_service
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.repositories.monitoring_snapshot_repository import (
    MonitoringSnapshotRepository,
)
from app.services.ssh_service import SSHService


class MonitoringService:

    def __init__(self, db):
        self.repository = MonitoringSnapshotRepository(db)

    def collect(self, server):

        password = encryption_service.decrypt(server.encrypted_password)

        with SSHService(
            hostname=server.hostname,
            username=server.username,
            password=password,
            port=server.ssh_port,
        ) as ssh:

            collector = CollectorFactory.create(
                server,
                ssh,
            )

            metrics = collector.collect()

            snapshot = MonitoringSnapshot(
                server_id=server.id,
                cpu_usage=metrics.cpu.usage_percent,
                memory_usage=metrics.memory.usage_percent,
                disk_usage=metrics.disk.usage_percent,
                load_average=metrics.load.load_1m,
                network_rx=metrics.network.total_rx,
                network_tx=metrics.network.total_tx,
                uptime_seconds=metrics.uptime_seconds,
            )

            self.repository.create(snapshot)

            return snapshot
