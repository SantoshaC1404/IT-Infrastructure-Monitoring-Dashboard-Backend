from app.dto.command.command_dto import Command
from app.commands.monitoring.base import BaseMonitoringCommandSet
from app.utils.enums import CommandShell


class WindowsMonitoringCommandSet(BaseMonitoringCommandSet):

    # CPU Usage
    def cpu_usage(self):
        return Command(
            command="Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage",
            shell=CommandShell.POWERSHELL,
        )

    # Memory Usage
    def memory_usage(self):
        return Command(
            "$os = Get-CimInstance Win32_OperatingSystem; [math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize) * 100, 4)",
            CommandShell.POWERSHELL,
        )

    # Disk Usage
    def disk_usage(self):
        return Command(
            "$disks = Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3'; $used = $disks | Measure-Object -Property Size -Sum | Select-Object -ExpandProperty Sum; $free = $disks | Measure-Object -Property FreeSpace -Sum | Select-Object -ExpandProperty Sum; [math]::Round((($used - $free) / $used) * 100, 4)",
            CommandShell.POWERSHELL,
        )

    # Uptime
    def uptime(self):
        return Command(
            "(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Select-Object -ExpandProperty TotalSeconds",
            CommandShell.POWERSHELL,
        )

    # Network Usage
    def network_usage(self):
        return Command(
            "Get-CimInstance Win32_PerfFormattedData_Tcpip_NetworkInterface | Select-Object Name,BytesReceivedPersec,BytesSentPersec",
            CommandShell.POWERSHELL,
        )

    # Load Average
    def load_average(self):
        return Command(
            "(Get-CimInstance Win32_PerfFormattedData_PerfOS_System).ProcessorQueueLength",
            CommandShell.POWERSHELL,
        )

    # Process Count
    def process_count(self):
        return Command(
            "(Get-Process).Count",
            CommandShell.POWERSHELL,
        )

    # Disk I/O
    def disk_io(self):
        return Command(
            "Get-CimInstance Win32_PerfFormattedData_PerfDisk_LogicalDisk -Filter \"Name='_Total'\" | Select-Object DiskReadBytesPersec,DiskWriteBytesPersec",
            CommandShell.POWERSHELL,
        )

    # Logged-in Users
    def logged_in_users(self):
        return Command(
            "(Get-CimInstance Win32_ComputerSystem).NumberOfLoggedOnUsers",
            CommandShell.POWERSHELL,
        )

    # Current Logged-in User
    def current_logged_in_user(self):
        return Command(
            command="(Get-CimInstance Win32_ComputerSystem).UserName",
            shell=CommandShell.POWERSHELL,
        )

    # Last Login Time
    def last_login(self):
        return Command(
            command="""
                Get-WinEvent -LogName Security -MaxEvents 1 `
                | Where-Object {$_.Id -eq 4624} `
                | Select-Object -ExpandProperty TimeCreated
                """,
            shell=CommandShell.POWERSHELL,
        )
