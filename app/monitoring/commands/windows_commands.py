from app.monitoring.commands.base import BaseMonitoringCommandSet


class WindowsMonitoringCommandSet(BaseMonitoringCommandSet):

    def cpu_usage(self):
        return "(Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue"

    def memory_usage(self):
        return """
        $os = Get-CimInstance Win32_OperatingSystem
        @{
            Total = $os.TotalVisibleMemorySize
            Free = $os.FreePhysicalMemory
        } | ConvertTo-Json -Compress
        """

    def disk_usage(self):
        return """
        Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" |
        Select-Object DeviceID, Size, FreeSpace |
        ConvertTo-Json -Compress
        """

    def network_usage(self):
        return """
        Get-NetAdapterStatistics |
        Select-Object Name, ReceivedBytes, SentBytes |
        ConvertTo-Json -Compress
        """

    def uptime(self):
        return """
        ((Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime).TotalSeconds
        """

    def load_average(self):
        return ""

    def process_count(self):
        return "(Get-Process).Count"
