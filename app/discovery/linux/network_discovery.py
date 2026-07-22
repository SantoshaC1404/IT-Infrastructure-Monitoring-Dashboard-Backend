from app.commands.discovery.factory import DiscoveryCommandsFactory
from app.dto.discovered_network import (
    DiscoveredNetworkInterface,
)
from app.utils.enums import DeviceType


class LinuxNetworkDiscovery:

    def __init__(self, connector):
        self.connector = connector
        self.commands = DiscoveryCommandsFactory.get(DeviceType.LINUX)

    def discover(self) -> list[DiscoveredNetworkInterface]:

        output = self.connector.execute(
            self.commands.network_interfaces(),
        )

        interfaces = []

        for line in output.splitlines():

            values = line.split()

            if len(values) < 2:
                continue

            interfaces.append(
                DiscoveredNetworkInterface(
                    interface_name=values[0],
                    ipv4_address=values[1].split("/")[0],
                    ipv6_address=None,
                    mac_address=None,
                    speed_mbps=None,
                    is_up=True,
                )
            )

        return interfaces
