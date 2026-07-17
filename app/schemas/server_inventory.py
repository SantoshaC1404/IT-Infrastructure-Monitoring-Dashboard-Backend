from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import ServerType


class ServerInventoryBase(BaseModel):

    hostname: str

    server_type: ServerType

    operating_system: str | None = None

    os_version: str | None = None

    kernel_version: str | None = None

    architecture: str | None = None

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

    # Disk
    total_disk_bytes: int | None = None

    # Hardware
    virtualization: str | None = None

    manufacturer: str | None = None

    model: str | None = None

    serial_number: str | None = None


class ServerInventoryResponse(ServerInventoryBase):

    id: int

    server_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
