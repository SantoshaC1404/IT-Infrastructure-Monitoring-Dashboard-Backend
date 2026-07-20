from app.discovery.commands.factory import DiscoveryCommandsFactory
from app.dto.discovered_inventory import DiscoveredInventory
from app.utils.enums import DeviceType


class LinuxInventoryDiscovery:

    def __init__(self, connector):
        self.connector = connector
        self.commands = DiscoveryCommandsFactory.get(DeviceType.LINUX)

    def discover(self) -> DiscoveredInventory:

        hostname = self.connector.execute(self.commands.hostname())

        operating_system = self.connector.execute(self.commands.operating_system())

        os_version = self.connector.execute(self.commands.os_version())

        kernel_version = self.connector.execute(self.commands.kernel_version())

        architecture = self.connector.execute(self.commands.architecture())

        cpu_model = self.connector.execute(self.commands.cpu_model()).strip()

        physical_cores = int(
            self.connector.execute(self.commands.physical_cores()) or 0
        )

        logical_cores = int(self.connector.execute(self.commands.logical_cores()) or 0)

        total_memory = (
            int(self.connector.execute(self.commands.total_memory()) or 0) * 1024
        )

        virtualization = self.connector.execute(self.commands.virtualization())

        return DiscoveredInventory(
            hostname=hostname,
            operating_system=operating_system,
            os_version=os_version,
            kernel_version=kernel_version,
            architecture=architecture,
            cpu_vendor=None,
            cpu_model=cpu_model,
            cpu_architecture=architecture,
            physical_cores=physical_cores,
            logical_cores=logical_cores,
            total_memory_bytes=total_memory,
            available_memory_bytes=0,
            used_memory_bytes=0,
            total_disk_bytes=0,
            virtualization=virtualization,
            manufacturer=None,
            model=None,
            serial_number=None,
        )
