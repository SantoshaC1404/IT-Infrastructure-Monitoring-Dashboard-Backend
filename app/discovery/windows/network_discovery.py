from app.commands.discovery.windows_commands import WindowsDiscoveryCommands
from app.dto.discovered_network import DiscoveredNetworkInterface


class WindowsNetworkDiscovery:

    def __init__(self, connector):

        self.connector = connector
        self.commands = WindowsDiscoveryCommands()

    def discover(self):
        # print("=" * 80)
        # print("WindowsNetworkDiscovery.discover() CALLED")
        # print(__file__)
        # print("=" * 80)

        output = self.connector.execute(
            self.commands.network_interfaces(),
        )

        interfaces = []

        lines = output.splitlines()

        for line in lines[2:]:

            cols = line.split()

            if len(cols) < 3:
                continue

            interfaces.append(
                DiscoveredNetworkInterface(
                    interface_name=cols[1],
                    ipv4_address=cols[0],
                    ipv6_address=None,
                    mac_address=None,
                    speed_mbps=None,
                    is_up=True,
                )
            )

        return interfaces
