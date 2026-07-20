from app.monitoring.parsers.base import BaseMetricsParser


class WindowsMetricsParser(BaseMetricsParser):

    def cpu_usage(self, output: str) -> float:
        lines = [x.strip() for x in output.splitlines() if x.strip()]

        return float(lines[-1])

    def memory_usage(self, output: str) -> float:
        """
        TODO:
        Parse:
            FreePhysicalMemory
            TotalVisibleMemorySize

        Return percentage used.
        """
        return 0.0

    def disk_usage(self, output: str) -> float:
        """
        TODO:
        Parse WMIC logicaldisk output.
        """
        return 0.0

    def network_usage(self, output: str):
        """
        TODO:
        Parse netstat -e output.
        """

        return 0, 0

    def uptime(self, output: str) -> int:
        """
        TODO:
        Parse 'net stats workstation'
        """
        return 0

    def load_average(self, output: str) -> float:
        return 0.0

    def process_count(self, output: str) -> int:
        return int(output.strip())
