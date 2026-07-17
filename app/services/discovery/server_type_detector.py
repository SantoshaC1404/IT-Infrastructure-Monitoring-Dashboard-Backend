from app.commands.discovery.factory import DiscoveryCommandFactory
from app.core.exceptions import InventoryDiscoveryException
from app.services.ssh_service import SSHService
from app.utils.enums import ServerType


class ServerTypeDetector:

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    def detect(self) -> ServerType:

        status, _, _ = self.ssh.execute_with_status("uname")

        if status == 0:
            return ServerType.LINUX

        status, _, _ = self.ssh.execute_with_status("ver")

        if status == 0:
            return ServerType.WINDOWS

        raise InventoryDiscoveryException("Unable to detect operating system.")
