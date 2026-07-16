from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MonitoringSnapshotResponse(BaseModel):

    id: int

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    network_rx: float

    network_tx: float

    uptime: int

    load_average: float | None

    process_count: int | None

    collected_at: datetime

    model_config = ConfigDict(from_attributes=True)
