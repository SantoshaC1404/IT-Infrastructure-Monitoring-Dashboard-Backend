from app.commands.discovery.base import BaseDiscoveryCommandSet
from app.dto.command_dto import Command
from app.utils.enums import CommandShell


class WindowsDiscoveryCommands(BaseDiscoveryCommandSet):

    def detect_os(self):
        return Command(
            "$PSVersionTable.PSVersion",
            CommandShell.POWERSHELL,
        )

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

    def cpu_vendor(self):
        return Command(
            "(Get-CimInstance Win32_Processor).Manufacturer",
            CommandShell.POWERSHELL,
        )

    def cpu_architecture(self):
        return Command(
            "(Get-CimInstance Win32_Processor).Architecture",
            CommandShell.POWERSHELL,
        )

    def physical_cores(self):
        # return Command(
        #     "(Get-CimInstance Win32_Processor).NumberOfCores",
        #     CommandShell.POWERSHELL,
        # )
        return Command(
            "(Get-CimInstance Win32_Processor | Measure-Object NumberOfCores -Sum).Sum",
            CommandShell.POWERSHELL,
        )

    def logical_cores(self):
        return Command(
            "(Get-CimInstance Win32_Processor | Measure-Object NumberOfLogicalProcessors -Sum).Sum",
            CommandShell.POWERSHELL,
        )

    def total_memory(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
            CommandShell.POWERSHELL,
        )

    def available_memory(self):
        return Command(
            "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory * 1024",
            CommandShell.POWERSHELL,
        )

    def manufacturer(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).Manufacturer",
            CommandShell.POWERSHELL,
        )

    def model(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).Model",
            CommandShell.POWERSHELL,
        )

    def serial_number(self):
        return Command(
            "(Get-CimInstance Win32_BIOS).SerialNumber",
            CommandShell.POWERSHELL,
        )

    def virtualization(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).HypervisorPresent",
            CommandShell.POWERSHELL,
        )

    def disk_inventory(self):
        return Command(
            """
            Get-CimInstance Win32_LogicalDisk |
            Where-Object {$_.DriveType -eq 3} |
            Select DeviceID,FileSystem,Size,FreeSpace
            """,
            CommandShell.POWERSHELL,
        )

    # def network_interfaces(self):
    #     return Command(
    #         """
    #         Get-NetIPAddress -AddressFamily IPv4 |
    #         Where-Object {$_.IPAddress -ne '127.0.0.1'}
    #         """,
    #         CommandShell.POWERSHELL,
    #     )
    def network_interfaces(self):
        return Command(
            """
            Get-NetIPAddress -AddressFamily IPv4 |
            Where-Object {$_.IPAddress -ne '127.0.0.1'} |
            Select-Object InterfaceAlias,IPAddress |
            ConvertTo-Json -Compress
            """,
            CommandShell.POWERSHELL,
        )
