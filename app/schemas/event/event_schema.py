from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import EventSeverity, EventType


class EventResponse(BaseModel):

    id: int

    device_id: int

    event_type: EventType

    severity: EventSeverity

    metric: str | None

    current_value: float | None

    threshold: float | None

    title: str

    message: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
