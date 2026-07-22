from app.dto.command_dto import Command
from app.commands.monitoring.base import BaseMonitoringCommandSet
from app.utils.enums import CommandShell


class WindowsMonitoringCommandSet(BaseMonitoringCommandSet):

    def cpu_usage(self):
        return Command(
            command="powershell "
            '"Get-CimInstance Win32_Processor | '
            'Select-Object -ExpandProperty LoadPercentage"',
            shell=CommandShell.POWERSHELL,
        )

    def memory_usage(self):
        return Command(
            "powershell "
            '"Get-CimInstance Win32_OperatingSystem | '
            'Select FreePhysicalMemory,TotalVisibleMemorySize"',
            CommandShell.POWERSHELL,
        )

    def disk_usage(self):
        return Command(
            "powershell " "\"Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3'\"",
            CommandShell.POWERSHELL,
        )

    def uptime(self):
        return Command(
            "powershell "
            '"(Get-Date) - '
            '(gcim Win32_OperatingSystem).LastBootUpTime"',
            CommandShell.POWERSHELL,
        )

    def network_usage(self):
        return Command(
            "powershell "
            '"Get-CimInstance Win32_PerfFormattedData_Tcpip_NetworkInterface | '
            'Select-Object Name,BytesReceivedPersec,BytesSentPersec"',
            CommandShell.POWERSHELL,
        )

    def load_average(self):
        return Command(
            "powershell "
            '"(Get-CimInstance Win32_PerfFormattedData_PerfOS_System).ProcessorQueueLength"',
            CommandShell.POWERSHELL,
        )

    def process_count(self):
        return Command(
            "powershell " '"(Get-Process).Count"',
            CommandShell.POWERSHELL,
        )

    def disk_io(self):
        return Command(
            "powershell "
            '"Get-CimInstance Win32_PerfFormattedData_PerfDisk_LogicalDisk -Filter \\"Name=\'_Total\'\\" | '
            'Select-Object DiskReadBytesPersec,DiskWriteBytesPersec"',
            CommandShell.POWERSHELL,
        )

    def logged_in_users(self):
        return Command(
            "powershell "
            '"(Get-CimInstance Win32_ComputerSystem).NumberOfLoggedOnUsers"',
            CommandShell.POWERSHELL,
        )
