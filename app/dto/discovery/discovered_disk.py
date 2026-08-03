from dataclasses import dataclass


@dataclass(slots=True)
class DiscoveredDisk:

    device_name: str

    filesystem: str

    mount_point: str

    total_bytes: int

    used_bytes: int

    free_bytes: int
