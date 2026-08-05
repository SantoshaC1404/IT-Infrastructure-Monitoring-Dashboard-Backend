from datetime import datetime
import re

from app.parsers.base import BaseMetricsParser


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
        if output is None:
            return 0.0

        text = output.strip()
        if not text:
            return 0.0

        try:
            return float(text)
        except ValueError:
            numbers = [float(n) for n in re.findall(r"\d+\.?\d*", text)]
            if len(numbers) >= 2:
                free, total = numbers[0], numbers[1]
                if total > 0:
                    return round((total - free) / total * 100, 4)
            return 0.0

    def disk_usage(self, output: str) -> float:
        if output is None:
            return 0.0

        text = output.strip()
        if not text:
            return 0.0

        try:
            return float(text)
        except ValueError:
            numbers = [float(n) for n in re.findall(r"\d+\.?\d*", text)]
            if len(numbers) >= 2:
                free, total = numbers[0], numbers[1]
                if total > 0:
                    return round((total - free) / total * 100, 4)
            return 0.0

    def network_usage(self, output: str):
        """
        TODO:
        Parse netstat -e output.
        """

        return 0, 0

    _timespan_pattern = re.compile(
        r"^(?:(?P<days>\d+)\.)?(?P<hours>\d{1,2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})(?:\.(?P<fraction>\d+))?$"
    )

    # windows uptime 
    def uptime(self, output: str) -> int:
        if output is None:
            return 0

        text = output.strip()
        if not text:
            return 0

        match = self._timespan_pattern.search(text)
        if match:
            days = int(match.group("days") or 0)
            hours = int(match.group("hours"))
            minutes = int(match.group("minutes"))
            seconds = int(match.group("seconds"))

            return days * 86400 + hours * 3600 + minutes * 60 + seconds

        try:
            return int(float(text))
        except ValueError:
            pass

        boot_time = self._parse_datetime(text)
        if boot_time is not None:
            now = datetime.now(boot_time.tzinfo) if boot_time.tzinfo else datetime.utcnow()
            delta = now - boot_time
            return int(delta.total_seconds())

        return 0

    def load_average(self, output: str) -> float:
        return 0.0

    def process_count(self, output: str) -> int:
        return int(output.strip())

    def current_logged_in_user(self, output: str):
        return self._normalize_text(output)

    def last_login(self, output: str):
        return self._parse_datetime(output)
