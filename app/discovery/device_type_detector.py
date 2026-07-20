from app.discovery.commands.factory import DiscoveryCommandFactory
from app.core.exceptions import InventoryDiscoveryException
from app.connectors.ssh.ssh_connector import SSHConnector
from app.utils.enums import DeviceType


class DeviceTypeDetector:

    def __init__(self, ssh: SSHConnector):
        self.ssh = ssh

    def detect(self) -> DeviceType:

        status, _, _ = self.ssh.execute_with_status("uname")

        if status == 0:
            return DeviceType.LINUX

        status, _, _ = self.ssh.execute_with_status("ver")

        if status == 0:
            return DeviceType.WINDOWS

        raise InventoryDiscoveryException("Unable to detect operating system.")
