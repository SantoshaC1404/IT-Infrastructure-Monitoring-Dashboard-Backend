from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import AlertSeverity, AlertStatus


class AlertResponse(BaseModel):

    id: int

    severity: AlertSeverity

    title: str

    message: str

    metric: str

    threshold: float

    current_value: float

    status: AlertStatus

    created_at: datetime

    acknowledged_at: datetime | None

    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
