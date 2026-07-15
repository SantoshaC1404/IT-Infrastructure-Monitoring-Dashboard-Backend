from dataclasses import dataclass


@dataclass(slots=True)
class DiscoveredNetworkInterface:

    interface_name: str

    mac_address: str | None

    ipv4_address: str | None

    ipv6_address: str | None

    speed_mbps: int | None

    is_up: bool
