from app.discovery.commands.base import BaseDiscoveryCommandSet
from app.dto.command_dto import Command, CommandShell


class LinuxDiscoveryCommands(BaseDiscoveryCommandSet):

    # Detection
    def detect_os(self):
        return Command("uname", CommandShell.SHELL)

    # Inventory
    def hostname(self):
        return Command("hostname", CommandShell.SHELL)

    def operating_system(self):
        return Command(
            "grep '^NAME=' /etc/os-release | " "cut -d= -f2 | tr -d '\"'",
            CommandShell.SHELL,
        )

    def os_version(self):
        return Command(
            "grep '^VERSION=' /etc/os-release | " "cut -d= -f2 | tr -d '\"'",
            CommandShell.SHELL,
        )

    def kernel_version(self):
        return Command("uname -r", CommandShell.SHELL)

    def architecture(self):
        return Command("hostname", CommandShell.SHELL)
        return "uname -m"

    def cpu_model(self):
        return Command(
            "lscpu | grep 'Model name' | " "cut -d: -f2",
            CommandShell.SHELL,
        )

    def physical_cores(self):
        return Command(
            "lscpu | grep '^Core(s) per socket:' | " "awk '{print $4}'",
            CommandShell.SHELL,
        )

    def logical_cores(self):
        return Command("nproc", CommandShell.SHELL)

    def total_memory(self):
        return Command(
            "grep MemTotal /proc/meminfo | " "awk '{print $2}'",
            CommandShell.SHELL,
        )

    def virtualization(self):
        return Command("systemd-detect-virt", CommandShell.SHELL)

    # Disk
    def disk_inventory(self):
        return Command(
            "lsblk -b -P -o NAME,FSTYPE,SIZE,MOUNTPOINT",
            CommandShell.SHELL,
        )

    # Network
    def network_interfaces(self):
        return Command(
            "ip -o -4 addr show | awk '{print $2,$4}'",
            CommandShell.SHELL,
        )
