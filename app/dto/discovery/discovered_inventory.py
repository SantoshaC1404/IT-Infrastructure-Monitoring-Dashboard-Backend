from dataclasses import dataclass


@dataclass(slots=True)
class DiscoveredInventory:
    # Device Identity
    hostname: str

    # Operating System
    operating_system: str
    os_version: str
    kernel_version: str
    architecture: str

    # CPU
    cpu_vendor: str | None = None
    cpu_model: str | None = None
    cpu_architecture: str | None = None

    physical_cores: int | None = None
    logical_cores: int | None = None

    # Memory
    total_memory_bytes: int | None = None
    available_memory_bytes: int | None = None
    used_memory_bytes: int | None = None

    # Storage
    total_disk_bytes: int | None = None

    # Hardware
    virtualization: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
