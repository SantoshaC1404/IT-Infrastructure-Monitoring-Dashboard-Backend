from app.discovery.linux.linux_discovery import LinuxDiscovery
from app.discovery.windows.windows_discovery import WindowsDiscovery

from app.utils.enums import DeviceType


class DiscoveryFactory:

    @staticmethod
    def create(
        device_type: DeviceType,
        connector,
    ):

        if device_type == DeviceType.LINUX:
            return LinuxDiscovery(connector)

        if device_type == DeviceType.WINDOWS:
            return WindowsDiscovery(connector)

        raise ValueError(f"Unsupported device type: {device_type}")
