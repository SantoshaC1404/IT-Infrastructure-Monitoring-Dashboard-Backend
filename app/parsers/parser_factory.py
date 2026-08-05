from app.parsers.base import BaseMonitoringParser
from app.parsers.linux_metrics_parser import LinuxMetricsParser
from app.parsers.windows_metric_parser import WindowsMetricsParser
from app.utils.enums import DeviceType


class ParserFactory:

    @staticmethod
    def create(
        device_type: DeviceType,
    ) -> BaseMonitoringParser:

        if device_type == DeviceType.LINUX:
            return LinuxMetricsParser()

        if device_type == DeviceType.WINDOWS:
            return WindowsMetricsParser()

        raise ValueError(f"Unsupported device type: {device_type}")
