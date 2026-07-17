from app.commands.discovery.base import BaseDiscoveryCommandSet
from app.commands.discovery.linux_commands import (
    LinuxDiscoveryCommands,
)
from app.commands.discovery.windows_commands import (
    WindowsDiscoveryCommands,
)
from app.utils.enums import ServerType


class DiscoveryCommandFactory:

    @staticmethod
    def get(
        server_type: ServerType,
    ) -> BaseDiscoveryCommandSet:

        if server_type == ServerType.LINUX:
            return LinuxDiscoveryCommands()

        if server_type == ServerType.WINDOWS:
            return WindowsDiscoveryCommands()

        raise ValueError(f"Unsupported server type: {server_type}")
