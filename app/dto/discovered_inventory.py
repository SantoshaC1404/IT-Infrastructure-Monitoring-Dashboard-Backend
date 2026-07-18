from dataclasses import dataclass

from app.utils.enums import DeviceType


@dataclass(slots=True)
class DiscoveredInventory:

    hostname: str

    server_type: DeviceType

    operating_system: str | None

    os_version: str | None

    kernel_version: str | None

    architecture: str | None

    # CPU
    cpu_vendor: str | None

    cpu_model: str | None

    cpu_architecture: str | None

    physical_cores: int | None

    logical_cores: int | None

    # Memory
    total_memory_bytes: int | None

    available_memory_bytes: int | None

    used_memory_bytes: int | None

    # Disk
    total_disk_bytes: int | None

    # Hardware
    virtualization: str | None

    manufacturer: str | None

    model: str | None

    serial_number: str | None
