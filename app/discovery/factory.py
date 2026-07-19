from app.discovery.linux.discovery_service import LinuxDiscoveryService
from app.discovery.windows.discovery_service import WindowsDiscoveryService

from app.utils.enums import DeviceType


class DiscoveryFactory:

    @staticmethod
    def create(device, connection):

        if device.device_type == DeviceType.LINUX_SERVER:
            return LinuxDiscoveryService(connection)

        if device.device_type == DeviceType.WINDOWS_SERVER:
            return WindowsDiscoveryService(connection)

        raise ValueError(f"Unsupported device type: {device.device_type}")
