from app.monitoring.collectors.linux_metrics_collector import LinuxMetricsCollector
from app.monitoring.collectors.windows_metrics_collector import WindowsMetricsCollector
from app.monitoring.commands.monitoring.factory import CommandFactory
from app.utils.enums import DeviceType


class CollectorFactory:

    @staticmethod
    def get(server_type: DeviceType, ssh):

        commands = CommandFactory.get(server_type)

        if server_type == DeviceType.LINUX:
            return LinuxMetricsCollector(ssh, commands)

        if server_type == DeviceType.WINDOWS:
            return WindowsMetricsCollector(ssh, commands)

        raise ValueError(f"Unsupported server type: {server_type}")
