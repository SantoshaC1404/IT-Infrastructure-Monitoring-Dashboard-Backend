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
from app.services.discovery.device_type_detector import (
    DeviceTypeDetector,
)
from app.connections.ssh.ssh_connection import SSHService


class DiscoveryService:

    def __init__(self, connection):
        self.connection = connection

    def discover(self) -> DiscoveryResult:

        device_type = DeviceTypeDetector(
            self.connection,
        ).detect()

        inventory = InventoryDiscoveryService(
            self.connection,
            device_type,
        ).discover()

        disks = DiskDiscoveryService(
            self.connection,
            device_type,
        ).discover()

        interfaces = NetworkInterfaceDiscoveryService(
            self.connection,
            device_type,
        ).discover()

        return DiscoveryResult(
            inventory=inventory,
            disks=disks,
            interfaces=interfaces,
        )
