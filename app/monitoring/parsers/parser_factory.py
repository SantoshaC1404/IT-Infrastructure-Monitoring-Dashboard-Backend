from app.monitoring.parsers.base import BaseMonitoringParser
from app.monitoring.parsers.linux_metrics_parser import LinuxMonitoringParser
from app.monitoring.parsers.windows_metric_parser import WindowsMonitoringParser
from app.utils.enums import DeviceType


class ParserFactory:

    @staticmethod
    def create(
        device_type: DeviceType,
    ) -> BaseMonitoringParser:

        if device_type == DeviceType.LINUX:
            return LinuxMonitoringParser()

        if device_type == DeviceType.WINDOWS:
            return WindowsMonitoringParser()

        raise ValueError(f"Unsupported device type: {device_type}")
