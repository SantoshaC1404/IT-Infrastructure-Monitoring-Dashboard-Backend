from datetime import datetime

from app.dto.monitoring_result import MonitoringResult
from app.monitoring.collectors.base import BaseMetricsCollector


class WindowsMetricsCollector(BaseMetricsCollector):

    def __init__(
        self,
        connector,
        commands,
    ):
        self.connector = connector
        self.commands = commands

    def collect(self) -> MonitoringResult:

        # TODO:
        # Parse actual Windows outputs.

        return MonitoringResult(
            cpu_usage=0,
            memory_usage=0,
            disk_usage=0,
            network_rx=0,
            network_tx=0,
            uptime=0,
            load_average=0,
            process_count=0,
            collected_at=datetime.utcnow(),
        )
