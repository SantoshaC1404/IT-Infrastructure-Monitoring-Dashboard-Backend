from app.discovery.commands.base import BaseDiscoveryCommandSet
from app.discovery.commands.linux_commands import (
    LinuxDiscoveryCommands,
)
from app.discovery.commands.windows_commands import (
    WindowsDiscoveryCommands,
)
from app.utils.enums import DeviceType


class DiscoveryCommandsFactory:

    @staticmethod
    def get(
        server_type: DeviceType,
    ) -> BaseDiscoveryCommandSet:

        if server_type == DeviceType.LINUX:
            return LinuxDiscoveryCommands()

        if server_type == DeviceType.WINDOWS:
            return WindowsDiscoveryCommands()

        raise ValueError(f"Unsupported server type: {server_type}")
