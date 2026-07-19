from app.monitoring.collectors.base import BaseMetricsCollector
from app.monitoring.collectors.linux_metrics_collector import (
    LinuxMetricsCollector,
)
from app.monitoring.collectors.windows_metrics_collector import (
    WindowsMetricsCollector,
)
from app.monitoring.commands.factory import MonitoringCommandsFactory
from app.utils.enums import DeviceType


class CollectorFactory:

    @staticmethod
    def create(
        device_type: DeviceType,
        connector,
    ) -> BaseMetricsCollector:

        commands = MonitoringCommandsFactory.get(device_type)

        if device_type == DeviceType.LINUX:
            return LinuxMetricsCollector(
                connector,
                commands,
            )

        if device_type == DeviceType.WINDOWS:
            return WindowsMetricsCollector(
                connector,
                commands,
            )

        raise ValueError(f"Unsupported device type: {device_type}")
