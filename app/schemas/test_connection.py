from pydantic import BaseModel

from app.utils.enums import DeviceType


class TestConnectionRequest(BaseModel):
    device_type: DeviceType
    ip_address: str
    username: str
    password: str
    port: int | None = None


class TestConnectionResponse(BaseModel):
    success: bool
    message: str
