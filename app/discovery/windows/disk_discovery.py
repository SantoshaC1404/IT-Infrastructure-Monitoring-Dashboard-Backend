# from app.commands.discovery.windows_commands import WindowsDiscoveryCommands
from app.commands.discovery.windows_commands import WindowsDiscoveryCommands
from app.dto.discovered_disk import DiscoveredDisk


class WindowsDiskDiscovery:

    def __init__(self, connector):

        self.connector = connector
        self.commands = WindowsDiscoveryCommands()

    def discover(self):

        output = self.connector.execute(
            self.commands.disk_inventory(),
        )

        disks = []

        lines = output.splitlines()

        #
        # Skip header
        #

        for line in lines[2:]:

            cols = line.split()

            if len(cols) < 4:
                continue

            device = cols[0]

            filesystem = cols[1]

            size = int(cols[2])

            free = int(cols[3])

            disks.append(
                DiscoveredDisk(
                    device_name=device,
                    filesystem=filesystem,
                    mount_point=device,
                    total_bytes=size,
                    free_bytes=free,
                    used_bytes=size - free,
                )
            )

        return disks
