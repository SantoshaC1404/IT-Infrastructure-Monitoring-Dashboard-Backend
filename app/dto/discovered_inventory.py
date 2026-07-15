from dataclasses import dataclass

from app.utils.enums import ServerType


@dataclass(slots=True)
class DiscoveredInventory:

    hostname: str

    server_type: ServerType

    operating_system: str | None

    os_version: str | None

    kernel_version: str | None

    architecture: str | None

    cpu_model: str | None

    physical_cores: int | None

    logical_cores: int | None

    total_memory_bytes: int | None

    virtualization: str | None

    manufacturer: str | None = None

    model: str | None = None

    serial_number: str | None = None
