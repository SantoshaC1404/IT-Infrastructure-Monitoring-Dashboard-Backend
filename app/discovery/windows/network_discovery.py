from app.discovery.commands.windows_commands import WindowsDiscoveryCommands

from app.dto.discovered_network import (
    DiscoveredNetworkInterface,
)


class WindowsNetworkDiscovery:

    def __init__(self, connector):

        self.connector = connector
        self.commands = WindowsDiscoveryCommands()

    def discover(self) -> list[DiscoveredNetworkInterface]:

        output = self.connector.execute(self.commands.network_interfaces())

        interfaces = []

        for line in output.splitlines():

            values = line.split(",")

            if len(values) < 2:
                continue

            interfaces.append(
                DiscoveredNetworkInterface(
                    interface_name=values[0],
                    ipv4_address=values[1],
                    ipv6_address=None,
                    mac_address=None,
                    speed_mbps=None,
                    is_up=True,
                )
            )

        return interfaces
