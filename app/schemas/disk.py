from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.network_interface import NetworkInterfaceBase
from app.schemas.device_inventory import DeviceInventoryBase


class DiskBase(BaseModel):
    device_name: str
    filesystem: str | None = None
    mount_point: str | None = None

    total_bytes: int = 0
    used_bytes: int = 0
    free_bytes: int = 0


class DiskCreate(DiskBase):
    pass


class DiskUpdate(BaseModel):
    filesystem: str | None = None
    mount_point: str | None = None

    total_bytes: int | None = None
    used_bytes: int | None = None
    free_bytes: int | None = None


class DiskResponse(DiskBase):
    id: int
    device_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiscoveryResult(BaseModel):
    inventory: DeviceInventoryBase
    disks: list[DiskBase]
    interfaces: list[NetworkInterfaceBase]
