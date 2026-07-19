from app.discovery.commands.windows_commands import WindowsDiscoveryCommands

from app.dto.discovered_disk import DiscoveredDisk


class WindowsDiskDiscovery:

    def __init__(self, connector):

        self.connector = connector
        self.commands = WindowsDiscoveryCommands()

    def discover(self) -> list[DiscoveredDisk]:

        output = self.connector.execute(self.commands.disks())

        disks = []

        for line in output.splitlines():

            values = line.split(",")

            if len(values) < 4:
                continue

            total = int(values[1]) if values[1] else 0
            free = int(values[2]) if values[2] else 0

            disks.append(
                DiscoveredDisk(
                    device_name=values[0],
                    filesystem=values[3],
                    mount_point=values[0],
                    total_bytes=total,
                    free_bytes=free,
                    used_bytes=total - free,
                )
            )

        return disks
