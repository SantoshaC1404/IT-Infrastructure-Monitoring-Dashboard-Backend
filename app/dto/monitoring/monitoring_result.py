from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MonitoringResult:

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    network_rx: int

    network_tx: int

    uptime: int

    load_average: float

    process_count: int

    collected_at: str

    login_source: str | None = None

    last_login_time: datetime | None = None
