from datetime import datetime

from app.connectors.base import BaseConnector
from app.dto.monitoring_result import MonitoringResult


class MetricsCollectorService:
    """
    Base metrics collector.

    Responsible only for:
        • Executing monitoring commands
        • Parsing generic numeric outputs
        • Returning MonitoringResult

    Does not know whether the connector is:
        - SSH
        - WinRM
        - SNMP
        - WMI
        - REST API
    """

    def __init__(
        self,
        connector: BaseConnector,
        command_set,
    ):
        self.connector = connector
        self.commands = command_set

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------

    def collect(self) -> MonitoringResult:

        rx, tx = self._network_usage()

        return MonitoringResult(
            cpu_usage=self._cpu_usage(),
            memory_usage=self._memory_usage(),
            disk_usage=self._disk_usage(),
            network_rx=rx,
            network_tx=tx,
            uptime=self._uptime(),
            load_average=self._load_average(),
            process_count=self._process_count(),
            collected_at=datetime.utcnow().isoformat(),
        )

    # ----------------------------------------------------
    # CPU
    # ----------------------------------------------------

    def _cpu_usage(self) -> float:

        output = self.connector.execute(self.commands.cpu_usage())

        return float(output.strip())

    # ----------------------------------------------------
    # Memory
    # ----------------------------------------------------

    def _memory_usage(self) -> float:

        output = self.connector.execute(self.commands.memory_usage())

        return float(output.strip())

    # ----------------------------------------------------
    # Disk
    # ----------------------------------------------------

    def _disk_usage(self) -> float:

        output = self.connector.execute(self.commands.disk_usage())

        return float(output.strip())

    # ----------------------------------------------------
    # Network
    # ----------------------------------------------------

    def _network_usage(self):

        output = self.connector.execute(self.commands.network_usage())

        rx = 0
        tx = 0

        for line in output.splitlines():

            values = line.split()

            rx += int(values[1])
            tx += int(values[9])

        return rx, tx

    # ----------------------------------------------------
    # Uptime
    # ----------------------------------------------------

    def _uptime(self):

        output = self.connector.execute(self.commands.uptime())

        return int(output.strip())

    # ----------------------------------------------------
    # Load Average
    # ----------------------------------------------------

    def _load_average(self):

        output = self.connector.execute(self.commands.load_average())

        return float(output.strip())

    # ----------------------------------------------------
    # Process Count
    # ----------------------------------------------------

    def _process_count(self):

        output = self.connector.execute(self.commands.process_count())

        return int(output.strip())
