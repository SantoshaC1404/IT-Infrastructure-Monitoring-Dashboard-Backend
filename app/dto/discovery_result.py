from dataclasses import dataclass

from app.dto.discovered_disk import DiscoveredDisk
from app.dto.discovered_inventory import DiscoveredInventory
from app.dto.discovered_network import (
    DiscoveredNetworkInterface,
)


@dataclass(slots=True)
class DiscoveryResult:

    inventory: DiscoveredInventory

    disks: list[DiscoveredDisk]

    interfaces: list[DiscoveredNetworkInterface]
