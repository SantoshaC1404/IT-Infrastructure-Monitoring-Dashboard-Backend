from app.dto.discovery_result import DiscoveryResult
from app.schemas.server_inventory import ServerInventoryBase
from app.schemas.disk import DiskBase
from app.schemas.network_interface import NetworkInterfaceBase
from app.services.ssh_service import SSHService
from app.core.exceptions import InventoryDiscoveryException
from app.utils.enums import ServerType


class DiscoveryService:
    """
    Discovers inventory information from a server.

    Responsibilities

    - Detect Linux / Windows
    - Collect OS information
    - Collect CPU information
    - Collect Memory information
    - Collect Disk information
    - Collect Network Interfaces

    Does NOT save anything into database.
    """

    def __init__(self, ssh: SSHService):
        self.ssh = ssh

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------

    def discover(self):

        server_type = self.detect_server_type()

        if server_type == ServerType.LINUX:
            return self._discover_linux()

        raise InventoryDiscoveryException("Windows discovery not implemented yet.")

    # ------------------------------------------------------------
    # Detect Server Type
    # ------------------------------------------------------------

    def detect_server_type(self):

        status, output, error = self.ssh.execute_with_status("uname")

        if status == 0:
            return ServerType.LINUX

        raise InventoryDiscoveryException("Unable to detect server type.")

    # ------------------------------------------------------------
    # Linux Discovery
    # ------------------------------------------------------------

    def _discover_linux(self):

        inventory = self.collect_inventory()

        disks = self.collect_disks()

        interfaces = self.collect_network_interfaces()

        return DiscoveryResult(
            inventory=inventory,
            disks=disks,
            interfaces=interfaces,
        )

    # ------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------

    def collect_inventory(self):

        hostname = self.ssh.execute("hostname")

        operating_system = self.ssh.execute(
            "grep '^NAME=' /etc/os-release | cut -d= -f2 | tr -d '\"'"
        )

        os_version = self.ssh.execute(
            "grep '^VERSION=' /etc/os-release | cut -d= -f2 | tr -d '\"'"
        )

        kernel = self.ssh.execute("uname -r")

        architecture = self.ssh.execute("uname -m")

        cpu_model = self.ssh.execute("lscpu | grep 'Model name' | cut -d: -f2").strip()

        physical = int(
            self.ssh.execute("lscpu | grep '^Core(s) per socket:' | awk '{print $4}'")
            or 0
        )

        logical = int(self.ssh.execute("nproc") or 0)

        total_memory = (
            int(self.ssh.execute("grep MemTotal /proc/meminfo | awk '{print $2}'") or 0)
            * 1024
        )

        virtualization = self.ssh.execute("systemd-detect-virt")

        return ServerInventoryBase(
            hostname=hostname,
            server_type=ServerType.LINUX,
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

    # ------------------------------------------------------------
    # Disks
    # ------------------------------------------------------------

    def collect_disks(self):

        command = "lsblk -b -P -o NAME,FSTYPE,SIZE,MOUNTPOINT"

        output = self.ssh.execute(command)

        disks = []

        for line in output.splitlines():

            values = {}

            for item in line.split():

                key, value = item.split("=")

                values[key] = value.replace('"', "")

            disks.append(
                DiskBase(
                    device_name=values.get("NAME", ""),
                    filesystem=values.get("FSTYPE"),
                    mount_point=values.get("MOUNTPOINT"),
                    total_bytes=int(values.get("SIZE", 0)),
                    used_bytes=0,
                    free_bytes=0,
                )
            )

        return disks

    # ------------------------------------------------------------
    # Network Interfaces
    # ------------------------------------------------------------

    def collect_network_interfaces(self):

        command = "ip -o -4 addr show | awk '{print $2,$4}'"

        output = self.ssh.execute(command)

        interfaces = []

        for line in output.splitlines():

            values = line.split()

            if len(values) < 2:
                continue

            interfaces.append(
                NetworkInterfaceBase(
                    interface_name=values[0],
                    ipv4_address=values[1].split("/")[0],
                    ipv6_address=None,
                    mac_address=None,
                    speed_mbps=None,
                    is_up=True,
                )
            )

        return interfaces
