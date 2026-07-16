from datetime import datetime

from app.dto.monitoring_result import MonitoringResult
from app.services.ssh_service import SSHService


class MetricsCollectorService:

    def __init__(self, ssh: SSHService, command_set):
        self.ssh = ssh
        self.command_set = command_set

    # -----------------------------------------

    def collect(self) -> MonitoringResult:

        cpu = self._cpu_usage()

        memory = self._memory_usage()

        disk = self._disk_usage()

        network = self._network_usage()

        uptime = self._uptime()

        load = self._load_average()

        processes = self._process_count()

        return MonitoringResult(
            cpu_usage=cpu,
            memory_usage=memory,
            disk_usage=disk,
            network_rx=network[0],
            network_tx=network[1],
            uptime=uptime,
            load_average=load,
            process_count=processes,
            collected_at=datetime.utcnow().isoformat(),
        )

    def _cpu_usage(self):
        output = self.ssh.execute(self.command_set.cpu_usage())

        return float(output.strip())

    def _memory_usage(self):
        output = self.ssh.execute(self.command_set.memory_usage())

        return float(output.strip())

    def _disk_usage(self):
        output = self.ssh.execute(self.command_set.disk_usage())

        return float(output.strip())

    def _load_average(self):
        output = self.ssh.execute(self.command_set.load_average())

        return float(output.strip())

    def _process_count(self):
        output = self.ssh.execute(self.command_set.process_count())

        return int(output.strip())

    def _uptime(self):
        output = self.ssh.execute(self.command_set.uptime())

        return int(output.strip())

    def _network_usage(self):
        output = self.ssh.execute(self.command_set.network_usage())

        rx = 0
        tx = 0

        for line in output.splitlines():
            values = line.split()
            rx += int(values[1])
            tx += int(values[9])

        return rx, tx
