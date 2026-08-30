from dataclasses import dataclass


@dataclass(slots=True)
class DashboardSummaryDTO:

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int

    monitoring_disabled: int

    critical_devices: int

    device_types: dict[str, int]

    cpu_usage: float = 0.0

    memory_usage: float = 0.0

    disk_usage: float = 0.0

    alerts: int = 0
