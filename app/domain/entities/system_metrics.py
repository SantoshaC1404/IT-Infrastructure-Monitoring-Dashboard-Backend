from dataclasses import dataclass


@dataclass
class CpuMetrics:
    usage_percent: float
    idle_percent: float


@dataclass
class MemoryMetrics:
    total_kb: int
    used_kb: int
    available_kb: int
    usage_percent: float


@dataclass
class DiskMetrics:
    total_bytes: int
    used_bytes: int
    available_bytes: int
    usage_percent: float


@dataclass
class LoadMetrics:
    load_1m: float
    load_5m: float
    load_15m: float


@dataclass
class SystemMetrics:
    cpu: CpuMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    load: LoadMetrics
    uptime_seconds: int
