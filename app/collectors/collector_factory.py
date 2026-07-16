from app.collectors.linux_metrics_collector import LinuxMetricsCollector
from app.collectors.windows_metrics_collector import WindowsMetricsCollector
from app.commands.factory import CommandFactory
from app.utils.enums import ServerType


class CollectorFactory:

    @staticmethod
    def get(server_type: ServerType, ssh):

        commands = CommandFactory.get(server_type)

        if server_type == ServerType.LINUX:
            return LinuxMetricsCollector(ssh, commands)

        if server_type == ServerType.WINDOWS:
            return WindowsMetricsCollector(ssh, commands)

        raise ValueError(f"Unsupported server type: {server_type}")
