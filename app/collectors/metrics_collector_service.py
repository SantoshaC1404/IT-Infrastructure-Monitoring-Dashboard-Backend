from datetime import datetime

from app.connectors.base import BaseConnector
from app.dto.monitoring.monitoring_result import MonitoringResult
from app.parsers.base import BaseMetricsParser


class MetricsCollectorService:
    """
    Collects monitoring metrics from a connected device.

    The connector executes operating-system commands while
    the parser converts raw command output into structured values.
    """

    def __init__(
        self,
        connector: BaseConnector,
        command_set,
        parser: BaseMetricsParser,
    ):
        self.connector = connector
        self.commands = command_set
        self.parser = parser

    def collect(self) -> MonitoringResult:
        outputs = {
            "cpu": self.connector.execute(self.commands.cpu_usage()),
            "memory": self.connector.execute(self.commands.memory_usage()),
            "disk": self.connector.execute(self.commands.disk_usage()),
            "network": self.connector.execute(self.commands.network_usage()),
            "uptime": self.connector.execute(self.commands.uptime()),
            "load": self.connector.execute(self.commands.load_average()),
            "processes": self.connector.execute(self.commands.process_count()),
            "login": self.connector.execute(self.commands.current_logged_in_user()),
            "last_login": self.connector.execute(self.commands.last_login()),
        }

        rx, tx = self.parser.network_usage(outputs["network"])

        return MonitoringResult(
            cpu_usage=self.parser.cpu_usage(outputs["cpu"]),
            memory_usage=self.parser.memory_usage(outputs["memory"]),
            disk_usage=self.parser.disk_usage(outputs["disk"]),
            network_rx=rx,
            network_tx=tx,
            uptime=self.parser.uptime(outputs["uptime"]),
            load_average=self.parser.load_average(outputs["load"]),
            process_count=self.parser.process_count(outputs["processes"]),
            login_source=self.parser.current_logged_in_user(outputs["login"]),
            last_login_time=self.parser.last_login(outputs["last_login"]),
            collected_at=datetime.utcnow().isoformat(),
        )
