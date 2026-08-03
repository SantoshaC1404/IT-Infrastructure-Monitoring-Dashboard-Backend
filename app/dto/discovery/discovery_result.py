from dataclasses import dataclass

from app.dto.discovery.discovered_disk import DiscoveredDisk
from app.dto.discovery.discovered_inventory import DiscoveredInventory
from app.dto.discovery.discovered_network import (
    DiscoveredNetworkInterface,
)
from app.utils.enums import DeviceType


@dataclass(slots=True)
class DiscoveryResult:

    device_type: DeviceType
    
    inventory: DiscoveredInventory

    disks: list[DiscoveredDisk]

    interfaces: list[DiscoveredNetworkInterface]
