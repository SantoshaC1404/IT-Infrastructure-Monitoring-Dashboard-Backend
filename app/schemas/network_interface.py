from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NetworkInterfaceBase(BaseModel):
    interface_name: str

    ipv4_address: str | None = None
    ipv6_address: str | None = None

    mac_address: str | None = None

    speed_mbps: int | None = None

    is_up: bool = True


class NetworkInterfaceCreate(NetworkInterfaceBase):
    pass


class NetworkInterfaceUpdate(BaseModel):
    ipv4_address: str | None = None
    ipv6_address: str | None = None

    mac_address: str | None = None

    speed_mbps: int | None = None

    is_up: bool | None = None


class NetworkInterfaceResponse(NetworkInterfaceBase):
    id: int
    device_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
