from app.dto.discovery_result import DiscoveryResult
from app.services.discovery.disk_discovery_service import (
    DiskDiscoveryService,
)
from app.services.discovery.inventory_discovery_service import (
    InventoryDiscoveryService,
)
from app.services.discovery.network_interface_discovery_service import (
    NetworkInterfaceDiscoveryService,
)
from app.services.discovery.server_type_detector import (
    DeviceTypeDetector,
)
from app.services.ssh_service import SSHService


class DiscoveryService:

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    def discover(self) -> DiscoveryResult:

        server_type = DeviceTypeDetector(
            self.ssh,
        ).detect()

        inventory = InventoryDiscoveryService(
            self.ssh,
            server_type,
        ).discover()

        disks = DiskDiscoveryService(
            self.ssh,
            server_type,
        ).discover()

        interfaces = NetworkInterfaceDiscoveryService(
            self.ssh,
            server_type,
        ).discover()

        return DiscoveryResult(
            inventory=inventory,
            disks=disks,
            interfaces=interfaces,
        )
