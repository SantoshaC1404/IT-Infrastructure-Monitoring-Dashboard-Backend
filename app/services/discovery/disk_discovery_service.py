from app.monitoring.commands.discovery.factory import DiscoveryCommandFactory
from app.schemas.disk import DiskBase
from app.services.ssh_service import SSHService
from app.utils.enums import DeviceType


class DiskDiscoveryService:

    def __init__(
        self,
        ssh: SSHService,
        server_type: DeviceType,
    ):
        self.ssh = ssh
        self.commands = DiscoveryCommandFactory.get(server_type)
        self.server_type = server_type

    def discover(self) -> list[DiskBase]:

        if self.server_type == DeviceType.LINUX:
            return self._discover_linux()

        return self._discover_windows()

    def _discover_linux(self):

        output = self.ssh.execute(self.commands.disk_inventory())

        disks = []

        for line in output.splitlines():

            values = {}

            for item in line.split():

                key, value = item.split("=")

                values[key] = value.replace('"', "")

            disks.append(
                DiskBase(
                    device_name=values.get("NAME"),
                    filesystem=values.get("FSTYPE"),
                    mount_point=values.get("MOUNTPOINT"),
                    total_bytes=int(values.get("SIZE", 0)),
                    used_bytes=0,
                    free_bytes=0,
                )
            )

        return disks

    def _discover_windows(self):
        # Implement parsing of WMIC output
        return []
