from datetime import datetime

from app.monitoring.collectors.base import BaseMetricsCollector
from app.dto.monitoring_result import MonitoringResult
from app.connections.ssh.ssh_connection import SSHService


class WindowsMetricsCollector(BaseMetricsCollector):

    def __init__(self, ssh: SSHService, commands):
        self.ssh = ssh
        self.commands = commands

    def collect(self):

        # TODO:
        # Parse Windows command outputs properly.

        return MonitoringResult(
            cpu_usage=0,
            memory_usage=0,
            disk_usage=0,
            network_rx=0,
            network_tx=0,
            uptime=0,
            load_average=0,
            process_count=0,
            collected_at=datetime.utcnow().isoformat(),
        )
