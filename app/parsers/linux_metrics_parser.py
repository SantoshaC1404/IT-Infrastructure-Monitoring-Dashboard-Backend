from datetime import datetime
import re

from app.parsers.base import BaseMetricsParser


class LinuxMetricsParser(BaseMetricsParser):

    @staticmethod
    def _float(value: str) -> float:
        value = value.strip()

        if not value:
            raise ValueError("Received empty metric output.")

        return float(value)

    def cpu_usage(self, output: str) -> float:
        return self._float(output)

    def memory_usage(self, output: str) -> float:
        return self._float(output)

    def disk_usage(self, output: str) -> float:
        return self._float(output)

    def load_average(self, output: str) -> float:
        return self._float(output)

    def uptime(self, output: str) -> int:
        return int(output.strip())

    def process_count(self, output: str) -> int:
        return int(output.strip())

    def network_usage(self, output: str) -> tuple[int, int]:
        rx = 0
        tx = 0

        for line in output.splitlines():
            values = line.split()

            if len(values) >= 10:
                rx += int(values[1])
                tx += int(values[9])

        return rx, tx

    def current_logged_in_user(self, output: str) -> str | None:

        line = output.strip()

        if not line:
            return None

        # Return the first IPv4 address found
        match = re.search(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            line,
        )

        if match:
            return match.group(0)

        return None

    def last_login(self, output: str):
        line = output.strip()

        if not line:
            return None

        parts = line.split()
        if len(parts) >= 8:
            try:
                date_str = " ".join(parts[3:8])
                return datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
            except ValueError:
                return line

        return line
