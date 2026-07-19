from app.discovery.base import BaseDiscovery
from app.discovery.windows.disk_discovery import WindowsDiskDiscovery
from app.discovery.windows.inventory_discovery import WindowsInventoryDiscovery
from app.discovery.windows.network_discovery import WindowsNetworkDiscovery
from app.dto.discovery_result import DiscoveryResult


class WindowsDiscovery(BaseDiscovery):

    def discover(self) -> DiscoveryResult:

        inventory = WindowsInventoryDiscovery(
            self.connection,
        ).discover()

        disks = WindowsDiskDiscovery(
            self.connection,
        ).discover()

        interfaces = WindowsNetworkDiscovery(
            self.connection,
        ).discover()

        return DiscoveryResult(
            inventory=inventory,
            disks=disks,
            interfaces=interfaces,
        )
