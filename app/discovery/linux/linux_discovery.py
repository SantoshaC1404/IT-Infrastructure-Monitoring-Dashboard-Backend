from app.discovery.base import BaseDiscovery
from app.discovery.linux.disk_discovery import LinuxDiskDiscovery
from app.discovery.linux.inventory_discovery import LinuxInventoryDiscovery
from app.discovery.linux.network_discovery import LinuxNetworkDiscovery
from app.dto.discovery_result import DiscoveryResult
from app.utils.enums import DeviceType


class LinuxDiscovery(BaseDiscovery):

    def discover(self) -> DiscoveryResult:

        inventory = LinuxInventoryDiscovery(
            self.connection,
        ).discover()

        disks = LinuxDiskDiscovery(
            self.connection,
        ).discover()

        interfaces = LinuxNetworkDiscovery(
            self.connection,
        ).discover()

        return DiscoveryResult(
            device_type=DeviceType.LINUX,
            inventory=inventory,
            disks=disks,
            interfaces=interfaces,
        )
