from app.discovery.commands.discovery.factory import DiscoveryCommandFactory
from app.core.exceptions import InventoryDiscoveryException
from app.connections.ssh.ssh_connection import SSHService
from app.utils.enums import DeviceType


class DeviceTypeDetector:

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    def detect(self) -> DeviceType:

        status, _, _ = self.ssh.execute_with_status("uname")

        if status == 0:
            return DeviceType.LINUX

        status, _, _ = self.ssh.execute_with_status("ver")

        if status == 0:
            return DeviceType.WINDOWS

        raise InventoryDiscoveryException("Unable to detect operating system.")
