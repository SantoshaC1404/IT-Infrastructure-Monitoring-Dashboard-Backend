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

    cpu_vendor: str | None = None

    cpu_model: str | None = None

    physical_cores: int | None = None

    logical_cores: int | None = None

    total_memory_bytes: int | None = None

    total_disk_bytes: int | None = None

    virtualization: str | None = None

    manufacturer: str | None = None

    model: str | None = None

    serial_number: str | None = None


class ServerInventoryResponse(ServerInventoryBase):

    id: int

    server_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)