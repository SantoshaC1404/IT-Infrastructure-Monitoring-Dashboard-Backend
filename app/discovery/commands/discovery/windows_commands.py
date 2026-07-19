from app.discovery.commands.discovery.base import BaseDiscoveryCommandSet


class WindowsDiscoveryCommands(BaseDiscoveryCommandSet):

    # Detection
    def detect_os(self):
        return "ver"

    # Inventory
    def hostname(self):
        return "hostname"

    def operating_system(self):
        return "(Get-CimInstance Win32_OperatingSystem).Caption"

    def os_version(self):
        return "(Get-CimInstance Win32_OperatingSystem).Version"

    def kernel_version(self):
        return "(Get-CimInstance Win32_OperatingSystem).BuildNumber"

    def architecture(self):
        return "(Get-CimInstance Win32_OperatingSystem).OSArchitecture"

    def cpu_model(self):
        return "(Get-CimInstance Win32_Processor).Name"

    def physical_cores(self):
        return "(Get-CimInstance Win32_Processor).NumberOfCores"

    def logical_cores(self):
        return "(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors"

    def total_memory(self):
        return "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"

    def virtualization(self):
        return "(Get-CimInstance Win32_ComputerSystem).Model"

    # Disk
    def disk_inventory(self):
        return "Get-CimInstance Win32_LogicalDisk"

    # Network
    def network_interfaces(self):
        return "Get-NetIPAddress"
