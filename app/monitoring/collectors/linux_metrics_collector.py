from datetime import datetime

from app.dto.monitoring_result import MonitoringResult
from app.monitoring.collectors.base import BaseMetricsCollector


class LinuxMetricsCollector(BaseMetricsCollector):

    def __init__(
        self,
        connector,
        commands,
    ):
        self.connector = connector
        self.commands = commands

    def collect(self) -> MonitoringResult:

        rx, tx = self.network_usage()

        return MonitoringResult(
            cpu_usage=self.cpu_usage(),
            memory_usage=self.memory_usage(),
            disk_usage=self.disk_usage(),
            network_rx=rx,
            network_tx=tx,
            uptime=self.uptime(),
            load_average=self.load_average(),
            process_count=self.process_count(),
            collected_at=datetime.utcnow(),
        )

    def cpu_usage(self):

        output = self.connector.execute(self.commands.cpu_usage())

        return float(output.strip())

    def memory_usage(self):

        output = self.connector.execute(self.commands.memory_usage())

        return float(output.strip())

    def disk_usage(self):

        output = self.connector.execute(self.commands.disk_usage())

        return float(output.strip())

    def load_average(self):

        output = self.connector.execute(self.commands.load_average())

        return float(output.strip())

    def process_count(self):

        output = self.connector.execute(self.commands.process_count())

        return int(output.strip())

    def uptime(self):

        output = self.connector.execute(self.commands.uptime())

        return int(output.strip())

    def network_usage(self):

        output = self.connector.execute(self.commands.network_usage())

        rx = 0
        tx = 0

        for line in output.splitlines():

            values = line.split()

            if len(values) < 10:
                continue

            rx += int(values[1])
            tx += int(values[9])

        return rx, tx
