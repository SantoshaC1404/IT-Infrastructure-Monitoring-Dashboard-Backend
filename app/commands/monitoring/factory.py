from app.commands.monitoring.base import BaseCommandSet
from app.commands.monitoring.linux_commands import LinuxCommandSet
from app.commands.monitoring.windows_commands import WindowsCommands
from app.utils.enums import ServerType


class CommandFactory:

    @staticmethod
    def get(server_type: ServerType) -> BaseCommandSet:

        if server_type == ServerType.LINUX:
            return LinuxCommandSet()

        if server_type == ServerType.WINDOWS:
            return WindowsCommands()

        raise ValueError(f"Unsupported server type: {server_type}")
