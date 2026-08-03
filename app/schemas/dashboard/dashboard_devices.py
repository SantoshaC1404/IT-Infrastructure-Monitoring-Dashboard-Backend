from pydantic import BaseModel


class DashboardDeviceResponse(BaseModel):
    id: int
    name: str
    ip_address: str
    status: str
    monitoring_enabled: bool
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class DashboardDevicesResponse(BaseModel):
    devices: list[DashboardDeviceResponse]
