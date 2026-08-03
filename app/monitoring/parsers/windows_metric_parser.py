from datetime import datetime

from app.monitoring.parsers.base import BaseMetricsParser


class WindowsMetricsParser(BaseMetricsParser):
    _datetime_formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%m/%d/%Y %I:%M:%S %p",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %I:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S.%f",
    )

    @staticmethod
    def _normalize_text(value: str | None) -> str | None:
        if value is None:
            return None

        text = value.strip()
        return text or None

    def _parse_datetime(self, value: str | datetime | None) -> datetime | None:
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            return None

        text = self._normalize_text(value)
        if text is None:
            return None

        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            pass

        for fmt in self._datetime_formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue

        return None

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

    def current_logged_in_user(self, output: str):
        return self._normalize_text(output)

    def last_login(self, output: str):
        return self._parse_datetime(output)
