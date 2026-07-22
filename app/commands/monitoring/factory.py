from app.commands.monitoring.base import BaseMonitoringCommandSet
from app.commands.monitoring.linux_commands import LinuxMonitoringCommandSet
from app.commands.monitoring.windows_commands import WindowsMonitoringCommandSet
from app.utils.enums import DeviceType


class MonitoringCommandsFactory:

    @staticmethod
    def get(device_type: DeviceType) -> BaseMonitoringCommandSet:

        if device_type == DeviceType.LINUX:
            return LinuxMonitoringCommandSet()

        if device_type == DeviceType.WINDOWS:
            return WindowsMonitoringCommandSet()

        raise ValueError(f"Unsupported device type: {device_type}")
