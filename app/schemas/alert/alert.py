from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import AlertSeverity, AlertStatus


class AlertResponse(BaseModel):

    id: int

    device_id: int

    device_name: str

    device_ip: str

    severity: AlertSeverity

    title: str

    message: str

    metric: str

    current_value: float

    threshold: float

    status: AlertStatus

    created_at: datetime

    acknowledged_at: datetime | None

    resolved_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )
