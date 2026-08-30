from typing import Dict

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int

    monitoring_disabled: int

    critical_devices: int

    alerts: int

    device_types: Dict[str, int]
