from app.discovery.commands.discovery.factory import DiscoveryCommandsFactory
from app.schemas.device_inventory import DeviceInventoryBase
from app.connections.ssh.ssh_connection import SSHService
from app.utils.enums import DeviceType


class InventoryDiscoveryService:

    def __init__(
        self,
        ssh: SSHService,
        device_type: DeviceType,
    ):
        self.ssh = ssh
        self.commands = DiscoveryCommandsFactory.get(device_type)
        self.device_type = device_type

    def discover(self) -> DeviceInventoryBase:

        hostname = self.ssh.execute(self.commands.hostname()).strip()

        operating_system = self.ssh.execute(self.commands.operating_system()).strip()

        os_version = self.ssh.execute(self.commands.os_version()).strip()

        kernel = self.ssh.execute(self.commands.kernel_version()).strip()

        architecture = self.ssh.execute(self.commands.architecture()).strip()

        cpu_model = self.ssh.execute(self.commands.cpu_model()).strip()

        physical = int(self.ssh.execute(self.commands.physical_cores()) or 0)

        logical = int(self.ssh.execute(self.commands.logical_cores()) or 0)

        total_memory = int(self.ssh.execute(self.commands.total_memory()) or 0)

        if self.device_type == DeviceType.LINUX:
            total_memory *= 1024

        virtualization = self.ssh.execute(self.commands.virtualization()).strip()

        return DeviceInventoryBase(
            hostname=hostname,
            device_type=self.device_type,
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
