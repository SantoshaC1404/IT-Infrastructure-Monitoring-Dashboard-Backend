from app.discovery.commands.windows_commands import WindowsDiscoveryCommands
from app.dto.discovered_inventory import DiscoveredInventory
from app.utils.enums import DeviceType


class WindowsInventoryDiscovery:

    def __init__(self, connector):

        self.connector = connector
        self.commands = WindowsDiscoveryCommands()

    def discover(self) -> DiscoveredInventory:

        hostname = self.connector.execute(self.commands.hostname())

        operating_system = self.connector.execute(self.commands.hostname())

        os_version = self.connector.execute(self.commands.os_version())

        architecture = self.connector.execute(self.commands.architecture())

        # cpu_vendor = self.connector.execute(self.commands.cpu_vendor())

        cpu_model = self.connector.execute(self.commands.cpu_model())

        physical_cores = int(
            self.connector.execute(self.commands.physical_cores()) or 0
        )

        logical_cores = int(self.connector.execute(self.commands.logical_cores()) or 0)

        total_memory = int(self.connector.execute(self.commands.total_memory()) or 0)

        # manufacturer = self.connector.execute(self.commands.manufacturer())

        model = self.connector.execute(self.commands.model())

        serial_number = self.connector.execute(self.commands.serial_number())

        return DiscoveredInventory(
            hostname=hostname,
            device_type=DeviceType.WINDOWS,
            operating_system=operating_system,
            os_version=os_version,
            kernel_version=None,
            architecture=architecture,
            # cpu_vendor=cpu_vendor,
            cpu_model=cpu_model,
            physical_cores=physical_cores,
            logical_cores=logical_cores,
            total_memory_bytes=total_memory,
            total_disk_bytes=None,
            virtualization=None,
            # manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
        )
