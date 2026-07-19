from app.discovery.linux.linux_discovery import LinuxDiscovery
from app.discovery.windows.windows_discovery import WindowsDiscovery
from app.utils.enums import DeviceType


class DiscoveryFactory:

    @staticmethod
    def create(
        request,
        connection,
    ):

        if request.device_type == DeviceType.LINUX:
            return LinuxDiscovery(connection)

        if request.device_type == DeviceType.WINDOWS:
            return WindowsDiscovery(connection)

        raise ValueError(f"Unsupported device type: {request.device_type}")
