from abc import ABC, abstractmethod

from app.dto.monitoring_result import MonitoringResult


class BaseMetricsCollector(ABC):

    @abstractmethod
    def collect(self) -> MonitoringResult:
        """Collect monitoring metrics."""
        pass
