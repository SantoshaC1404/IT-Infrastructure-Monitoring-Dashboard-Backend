from app.monitoring.commands.discovery.base import BaseDiscoveryCommandSet


class LinuxDiscoveryCommands(BaseDiscoveryCommandSet):

    # Detection
    def detect_os(self):
        return "uname"

    # Inventory
    def hostname(self):
        return "hostname"

    def operating_system(self):
        return "grep '^NAME=' /etc/os-release | " "cut -d= -f2 | tr -d '\"'"

    def os_version(self):
        return "grep '^VERSION=' /etc/os-release | " "cut -d= -f2 | tr -d '\"'"

    def kernel_version(self):
        return "uname -r"

    def architecture(self):
        return "uname -m"

    def cpu_model(self):
        return "lscpu | grep 'Model name' | " "cut -d: -f2"

    def physical_cores(self):
        return "lscpu | grep '^Core(s) per socket:' | " "awk '{print $4}'"

    def logical_cores(self):
        return "nproc"

    def total_memory(self):
        return "grep MemTotal /proc/meminfo | " "awk '{print $2}'"

    def virtualization(self):
        return "systemd-detect-virt"

    # Disk
    def disk_inventory(self):
        return "lsblk -b -P -o NAME,FSTYPE,SIZE,MOUNTPOINT"

    # Network
    def network_interfaces(self):
        return "ip -o -4 addr show | awk '{print $2,$4}'"
