from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import ServerType, ServerStatus


class ServerBase(BaseModel):
    name: str = Field(
        ...,
        title="Server Name",
        min_length=2,
        max_length=100,
    )

    hostname: str = Field(
        ...,
        title="Server Hostname",
        min_length=2,
        max_length=255,
    )

    ip_address: str = Field(
        ...,
        title="Server IP Address",
        min_length=7,
        max_length=50,
    )

    ssh_port: int = Field(
        default=22,
        title="SSH Port",
        ge=1,
        le=65535,
    )

    username: str = Field(
        ...,
        title="SSH Username",
        min_length=2,
        max_length=100,
    )

    server_type: ServerType = Field(
        ...,
        title="Server Type",
    )


class ServerCreate(ServerBase):
    password: str = Field(
        ...,
        title="SSH Password",
        min_length=6,
        max_length=255,
    )


class ServerUpdate(BaseModel):
    name: str | None = None
    hostname: str | None = None
    ip_address: str | None = None
    ssh_port: int | None = None
    username: str | None = None
    server_type: ServerType | None = None
    password: str | None = None
    monitoring_enabled: bool | None = None


class ServerResponse(ServerBase):
    id: int
    status: ServerStatus
    monitoring_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
