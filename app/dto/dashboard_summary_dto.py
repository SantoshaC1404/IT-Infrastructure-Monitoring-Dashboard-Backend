from dataclasses import dataclass


@dataclass(slots=True)
class DashboardSummaryDTO:

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int
