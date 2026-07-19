from app.discovery.commands.factory import DiscoveryCommandsFactory
from app.dto.discovered_disk import DiscoveredDisk
from app.utils.enums import DeviceType


class LinuxDiskDiscovery:

    def __init__(self, connector):
        self.connector = connector
        self.commands = DiscoveryCommandsFactory.get(DeviceType.LINUX)

    def discover(self) -> list[DiscoveredDisk]:

        output = self.connector.execute(self.commands.disk_inventory())

        disks = []

        for line in output.splitlines():

            values = {}

            for item in line.split():

                key, value = item.split("=")

                values[key] = value.replace('"', "")

            disks.append(
                DiscoveredDisk(
                    device_name=values.get("NAME", ""),
                    filesystem=values.get("FSTYPE"),
                    mount_point=values.get("MOUNTPOINT"),
                    total_bytes=int(values.get("SIZE", 0)),
                    used_bytes=0,
                    free_bytes=0,
                )
            )

        return disks
