from datetime import datetime

from app.commands.monitoring.base import BaseCommandSet
from app.dto.monitoring_result import MonitoringResult
from app.parsers.cpu_parser import CpuParser
from app.parsers.disk_parser import DiskParser
from app.parsers.load_parser import LoadParser
from app.parsers.memory_parser import MemoryParser
from app.parsers.network_parser import NetworkParser
from app.parsers.process_parser import ProcessParser
from app.parsers.uptime_parser import UptimeParser
from app.services.ssh_service import SSHService


class MetricsCollectorService:

    def __init__(
        self,
        ssh: SSHService,
        command_set: BaseCommandSet,
    ):
        self.ssh = ssh
        self.commands = command_set

    def collect(self) -> MonitoringResult:

        cpu = CpuParser.parse(self.ssh.execute(self.commands.cpu_usage))

        memory = MemoryParser.parse(self.ssh.execute(self.commands.memory_usage))

        disk = DiskParser.parse(self.ssh.execute(self.commands.disk_usage))

        load = LoadParser.parse(self.ssh.execute(self.commands.load_average))

        processes = ProcessParser.parse(self.ssh.execute(self.commands.process_count))

        uptime = UptimeParser.parse(self.ssh.execute(self.commands.uptime))

        rx, tx = NetworkParser.parse(self.ssh.execute(self.commands.network_usage))

        return MonitoringResult(
            cpu_usage=cpu,
            memory_usage=memory,
            disk_usage=disk,
            network_rx=rx,
            network_tx=tx,
            uptime=uptime,
            load_average=load,
            process_count=processes,
            collected_at=datetime.utcnow().isoformat(),
        )
