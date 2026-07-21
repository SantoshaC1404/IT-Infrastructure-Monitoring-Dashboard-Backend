from app.discovery.commands.base import BaseDiscoveryCommandSet
from app.dto.command_dto import Command, CommandShell


class WindowsDiscoveryCommands(BaseDiscoveryCommandSet):

    # Detection
    def detect_os(self):
        return Command("ver", CommandShell.POWERSHELL)

    # Inventory
    def hostname(self):
        return Command(
            "$env:COMPUTERNAME",
            CommandShell.POWERSHELL,
        )

    def operating_system(self):
        return Command(
            "(Get-CimInstance Win32_OperatingSystem).Caption",
            CommandShell.POWERSHELL,
        )

    def os_version(self):
        return Command(
            "(Get-CimInstance Win32_OperatingSystem).Version",
            CommandShell.POWERSHELL,
        )

    def kernel_version(self):
        return Command(
            "(Get-CimInstance Win32_OperatingSystem).BuildNumber",
            CommandShell.POWERSHELL,
        )

    def architecture(self):
        return Command(
            "(Get-CimInstance Win32_OperatingSystem).OSArchitecture",
            CommandShell.POWERSHELL,
        )

    def cpu_model(self):
        return Command(
            "(Get-CimInstance Win32_Processor).Name",
            CommandShell.POWERSHELL,
        )

    def physical_cores(self):
        return Command(
            "(Get-CimInstance Win32_Processor).NumberOfCores",
            CommandShell.POWERSHELL,
        )

    def logical_cores(self):
        return Command(
            "(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors",
            CommandShell.POWERSHELL,
        )

    def total_memory(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
            CommandShell.POWERSHELL,
        )

    def virtualization(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).Model",
            CommandShell.POWERSHELL,
        )

    # Disk
    def disk_inventory(self):
        return Command(
            "Get-CimInstance Win32_LogicalDisk",
            CommandShell.POWERSHELL,
        )

    # Network
    def network_interfaces(self):
        return Command("Get-NetIPAddress", CommandShell.POWERSHELL)
