from dataclasses import dataclass


@dataclass(slots=True)
class CriticalDevicesDTO:
    id: int

    name: str

    ip_address: str

    status: str

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    critical_reason: str
