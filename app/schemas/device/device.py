from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import DeviceStatus, DeviceType


class DeviceBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    ip_address: str = Field(
        ...,
        min_length=7,
        max_length=50,
    )

    ssh_port: int = Field(
        default=22,
        ge=1,
        le=65535,
    )

    username: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )


class DeviceCreate(DeviceBase):

    password: str = Field(
        ...,
        min_length=6,
        max_length=255,
    )

    device_type: DeviceType


class DeviceUpdate(BaseModel):

    name: str | None = None

    ip_address: str | None = None

    ssh_port: int | None = None

    username: str | None = None

    password: str | None = None

    monitoring_enabled: bool | None = None

    device_type: DeviceType | None = None


class DeviceResponse(DeviceBase):

    id: int

    monitoring_enabled: bool

    status: DeviceStatus

    last_seen: datetime | None

    cpu_usage: float | None = 0.0

    memory_usage: float | None = 0.0

    disk_usage: float | None = 0.0

    uptime: int | None = None

    login_source: str | None = None

    last_login_time: datetime | None = None

    created_at: datetime

    updated_at: datetime

    # Critical device information
    critical_reasons: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
