from pydantic import BaseModel


class DeviceTypeSummary(BaseModel):

    LINUX: int = 0

    WINDOWS: int = 0

    NETWORK: int = 0


class DashboardSummaryResponse(BaseModel):

    total_devices: int

    online_devices: int

    offline_devices: int

    monitoring_enabled: int

    monitoring_disabled: int

    device_types: DeviceTypeSummary
