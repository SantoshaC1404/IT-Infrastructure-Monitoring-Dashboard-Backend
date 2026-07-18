from app.monitoring.commands.discovery.base import BaseDiscoveryCommandSet


class WindowsDiscoveryCommands(BaseDiscoveryCommandSet):

    # Detection
    def detect_os(self):
        return "ver"

    # Inventory
    def hostname(self):
        return "hostname"

    def operating_system(self):
        return "wmic os get Caption /value"

    def os_version(self):
        return "wmic os get Version /value"

    def kernel_version(self):
        return "wmic os get BuildNumber /value"

    def architecture(self):
        return "wmic os get OSArchitecture /value"

    def cpu_model(self):
        return "wmic cpu get Name"

    def physical_cores(self):
        return "wmic cpu get NumberOfCores"

    def logical_cores(self):
        return "wmic cpu get NumberOfLogicalProcessors"

    def total_memory(self):
        return "wmic ComputerSystem get TotalPhysicalMemory"

    def virtualization(self):
        return "wmic computersystem get Model"

    # Disk
    def disk_inventory(self):
        return "wmic logicaldisk get " "DeviceID,FileSystem,Size,FreeSpace"

    # Network
    def network_interfaces(self):
        return (
            "wmic nicconfig where IPEnabled=true "
            "get Description,IPAddress,MACAddress"
        )
