from pydantic import BaseModel
from typing import Dict


class DashboardSummaryResponse(BaseModel):

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int

    monitoring_disabled: int

    device_types: Dict[str, int]
