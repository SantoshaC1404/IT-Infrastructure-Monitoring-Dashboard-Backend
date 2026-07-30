from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int
