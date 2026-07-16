from app.commands.base import BaseCommandSet


class WindowsCommands(BaseCommandSet):

    def cpu_usage(self):
        return "wmic cpu get loadpercentage"

    def memory_usage(self):
        return "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize"

    def disk_usage(self):
        return "wmic logicaldisk get size,freespace"

    def network_usage(self):
        return "netstat -e"

    def uptime(self):
        return "net stats workstation"

    def load_average(self):
        return ""

    def process_count(self):
        return 'tasklist | find /c /v ""'
