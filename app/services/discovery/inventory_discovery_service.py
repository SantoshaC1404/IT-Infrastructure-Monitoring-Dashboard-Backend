from app.monitoring.commands.discovery.factory import DiscoveryCommandFactory
from app.schemas.server_inventory import ServerInventoryBase
from app.services.ssh_service import SSHService
from app.utils.enums import DeviceType


class InventoryDiscoveryService:

    def __init__(
        self,
        ssh: SSHService,
        server_type: DeviceType,
    ):
        self.ssh = ssh
        self.commands = DiscoveryCommandFactory.get(server_type)
        self.server_type = server_type

    def discover(self) -> ServerInventoryBase:

        hostname = self.ssh.execute(self.commands.hostname()).strip()

        operating_system = self.ssh.execute(self.commands.operating_system()).strip()

        os_version = self.ssh.execute(self.commands.os_version()).strip()

        kernel = self.ssh.execute(self.commands.kernel_version()).strip()

        architecture = self.ssh.execute(self.commands.architecture()).strip()

        cpu_model = self.ssh.execute(self.commands.cpu_model()).strip()

        physical = int(self.ssh.execute(self.commands.physical_cores()) or 0)

        logical = int(self.ssh.execute(self.commands.logical_cores()) or 0)

        total_memory = int(self.ssh.execute(self.commands.total_memory()) or 0)

        if self.server_type == DeviceType.LINUX:
            total_memory *= 1024

        virtualization = self.ssh.execute(self.commands.virtualization()).strip()

        return ServerInventoryBase(
            hostname=hostname,
            server_type=self.server_type,
            operating_system=operating_system,
            os_version=os_version,
            kernel_version=kernel,
            architecture=architecture,
            cpu_model=cpu_model,
            physical_cores=physical,
            logical_cores=logical,
            total_memory_bytes=total_memory,
            virtualization=virtualization,
        )
