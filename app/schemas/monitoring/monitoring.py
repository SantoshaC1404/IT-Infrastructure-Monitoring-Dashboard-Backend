from datetime import datetime

from pydantic import BaseModel


class CpuMetrics(BaseModel):
    usage_percent: float
    idle_percent: float


class MemoryMetrics(BaseModel):
    total_mb: int
    used_mb: int
    free_mb: int
    available_mb: int
    usage_percent: float


class DiskPartition(BaseModel):
    filesystem: str
    mount_point: str
    total: str
    used: str
    available: str
    usage_percent: int


class DiskMetrics(BaseModel):
    partitions: list[DiskPartition]


class SystemInfo(BaseModel):
    hostname: str
    kernel: str
    uptime: str


class NetworkInterface(BaseModel):
    interface: str
    rx_bytes: int
    tx_bytes: int


class NetworkMetrics(BaseModel):
    interfaces: list[NetworkInterface]


class DockerContainer(BaseModel):
    container_id: str
    name: str
    image: str
    status: str


class DockerMetrics(BaseModel):
    containers: list[DockerContainer]


class ServiceStatus(BaseModel):
    service_name: str
    status: str


class ServiceMetrics(BaseModel):
    services: list[ServiceStatus]
