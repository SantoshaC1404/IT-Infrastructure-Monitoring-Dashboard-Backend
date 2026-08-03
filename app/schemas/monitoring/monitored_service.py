from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MonitoredServiceResponse(BaseModel):

    id: int

    service_name: str

    status: str

    enabled: bool

    last_checked: datetime

    model_config = ConfigDict(from_attributes=True)
