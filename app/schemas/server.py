from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.utils.enums import ServerType, ServerStatus


class ServerCreate(BaseModel):
    name: str
    hostname: str
    ip_address: str
    ssh_port: int = 22
    username: str
    password: str
    server_type: ServerType
    # monitoring_enabled: bool = True
    # status: ServerStatus = ServerStatus.UNKNOWN


class ServerResponse(BaseModel):
    id: int
    status: ServerStatus
    monitoring_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
