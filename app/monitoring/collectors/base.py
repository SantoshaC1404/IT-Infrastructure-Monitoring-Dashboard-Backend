from abc import ABC, abstractmethod

# class BaseCollector(ABC):

#     @abstractmethod
#     def collect(self):
#         raise NotImplementedError
# from abc import ABC, abstractmethod

from app.dto.monitoring_result import MonitoringResult


class BaseMetricsCollector(ABC):

    @abstractmethod
    def collect(self) -> MonitoringResult:
        pass
