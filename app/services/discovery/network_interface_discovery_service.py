from app.monitoring.commands.discovery.factory import DiscoveryCommandFactory
from app.schemas.network_interface import NetworkInterfaceBase
from app.connections.ssh.ssh_connection import SSHService
from app.utils.enums import DeviceType


class NetworkInterfaceDiscoveryService:

    def __init__(
        self,
        ssh: SSHService,
        device_type: DeviceType,
    ):
        self.ssh = ssh
        self.commands = DiscoveryCommandFactory.get(device_type)
        self.device_type = device_type

    def discover(self) -> list[NetworkInterfaceBase]:

        if self.device_type == DeviceType.LINUX:
            return self._discover_linux()

        return self._discover_windows()

    def _discover_linux(self):

        output = self.ssh.execute(self.commands.network_interfaces())

        interfaces = []

        for line in output.splitlines():

            values = line.split()

            if len(values) < 2:
                continue

            interfaces.append(
                NetworkInterfaceBase(
                    interface_name=values[0],
                    ipv4_address=values[1].split("/")[0],
                    ipv6_address=None,
                    mac_address=None,
                    speed_mbps=None,
                    is_up=True,
                )
            )

        return interfaces

    def _discover_windows(self):
        # Implement WMIC parsing
        return []
