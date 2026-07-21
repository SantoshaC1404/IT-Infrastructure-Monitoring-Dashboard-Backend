from app.monitoring.commands.base import BaseMonitoringCommandSet


class WindowsMonitoringCommandSet(BaseMonitoringCommandSet):

    def cpu_usage(self):
        return (
            "powershell "
            '"Get-CimInstance Win32_Processor | '
            'Select-Object -ExpandProperty LoadPercentage"'
        )

    def memory_usage(self):
        return (
            "powershell "
            '"Get-CimInstance Win32_OperatingSystem | '
            'Select FreePhysicalMemory,TotalVisibleMemorySize"'
        )

    def disk_usage(self):
        return (
            "powershell " "\"Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3'\""
        )

    def uptime(self):
        return (
            "powershell "
            '"(Get-Date) - '
            '(gcim Win32_OperatingSystem).LastBootUpTime"'
        )

    def network_usage(self):
        return (
            "powershell "
            '"Get-CimInstance Win32_PerfFormattedData_Tcpip_NetworkInterface | '
            'Select-Object Name,BytesReceivedPersec,BytesSentPersec"'
        )

    def load_average(self):
        return (
            "powershell "
            '"(Get-CimInstance Win32_PerfFormattedData_PerfOS_System).ProcessorQueueLength"'
        )

    def process_count(self):
        return "powershell " '"(Get-Process).Count"'

    def disk_io(self):
        return (
            "powershell "
            '"Get-CimInstance Win32_PerfFormattedData_PerfDisk_LogicalDisk -Filter \\"Name=\'_Total\'\\" | '
            'Select-Object DiskReadBytesPersec,DiskWriteBytesPersec"'
        )

    def logged_in_users(self):
        return (
            "powershell "
            '"(Get-CimInstance Win32_ComputerSystem).NumberOfLoggedOnUsers"'
        )
