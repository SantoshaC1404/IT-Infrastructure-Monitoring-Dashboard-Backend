from app.monitoring.commands.monitoring.base import BaseCommandSet
from app.monitoring.commands.monitoring.linux_commands import LinuxCommandSet
from app.monitoring.commands.monitoring.windows_commands import WindowsCommands
from app.utils.enums import DeviceType


class CommandFactory:

    @staticmethod
    def get(server_type: DeviceType) -> BaseCommandSet:

        if server_type == DeviceType.LINUX:
            return LinuxCommandSet()

        if server_type == DeviceType.WINDOWS:
            return WindowsCommands()

        raise ValueError(f"Unsupported server type: {server_type}")
