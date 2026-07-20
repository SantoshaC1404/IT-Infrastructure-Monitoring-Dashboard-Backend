from app.monitoring.parsers.base import BaseMetricsParser


class LinuxMetricsParser(BaseMetricsParser):

    def cpu_usage(self, output: str) -> float:
        return float(output.strip())

    def memory_usage(self, output: str) -> float:
        return float(output.strip())

    def disk_usage(self, output: str) -> float:
        return float(output.strip())

    def uptime(self, output: str) -> int:
        return int(output.strip())

    def load_average(self, output: str) -> float:
        return float(output.strip())

    def process_count(self, output: str) -> int:
        return int(output.strip())

    def network_usage(self, output: str) -> tuple[int, int]:

        rx = 0
        tx = 0

        for line in output.splitlines():

            values = line.split()

            if len(values) < 10:
                continue

            rx += int(values[1])
            tx += int(values[9])

        return rx, tx
