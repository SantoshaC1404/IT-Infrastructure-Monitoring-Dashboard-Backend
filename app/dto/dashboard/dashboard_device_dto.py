from dataclasses import dataclass


@dataclass(slots=True)
class DashboardDeviceDTO:

    id: int

    name: str

    ip_address: str

    status: str

    monitoring_enabled: bool

    cpu_usage: float

    memory_usage: float

    disk_usage: float
