from pydantic import BaseModel


class CriticalDeviceResponse(BaseModel):
    id: int

    name: str

    ip_address: str

    status: str

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    critical_reason: str


class CriticalDevicesResponse(BaseModel):
    critical_devices: list[CriticalDeviceResponse]
