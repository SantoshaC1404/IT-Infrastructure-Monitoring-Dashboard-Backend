from datetime import datetime

from app.connectors.base import BaseConnector
from app.dto.monitoring.monitoring_result import MonitoringResult
from app.monitoring.parsers.base import BaseMetricsParser


class MetricsCollectorService:
    """
    Executes monitoring commands and delegates all parsing
    to the operating-system specific parser.
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

        cpu = self.connector.execute(self.commands.cpu_usage())

        memory = self.connector.execute(self.commands.memory_usage())

        disk = self.connector.execute(self.commands.disk_usage())

        network = self.connector.execute(self.commands.network_usage())

        uptime = self.connector.execute(self.commands.uptime())

        load = self.connector.execute(self.commands.load_average())

        processes = self.connector.execute(self.commands.process_count())

        rx, tx = self.parser.network_usage(network)

        login_source = self.connector.execute(self.commands.current_logged_in_user())

        print("RAW LOGIN SOURCE:", repr(login_source))

        parsed_login_source = self.parser.current_logged_in_user(login_source)

        print("PARSED LOGIN SOURCE:", parsed_login_source)

        last_login = self.connector.execute(self.commands.last_login())

        return MonitoringResult(
            cpu_usage=self.parser.cpu_usage(cpu),
            memory_usage=self.parser.memory_usage(memory),
            disk_usage=self.parser.disk_usage(disk),
            network_rx=rx,
            network_tx=tx,
            uptime=self.parser.uptime(uptime),
            load_average=self.parser.load_average(load),
            process_count=self.parser.process_count(processes),
            collected_at=datetime.utcnow().isoformat(),
            login_source=parsed_login_source,
            last_login_time=self.parser.last_login(last_login),
        )
