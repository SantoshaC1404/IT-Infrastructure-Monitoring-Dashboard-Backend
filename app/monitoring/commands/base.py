from abc import ABC, abstractmethod


class BaseMonitoringCommandSet(ABC):
    """Base class for monitoring command sets."""

    @abstractmethod
    def cpu_usage(self) -> str:
        pass

    @abstractmethod
    def memory_usage(self) -> str:
        pass

    @abstractmethod
    def disk_usage(self) -> str:
        pass

    @abstractmethod
    def network_usage(self) -> str:
        pass

    @abstractmethod
    def uptime(self) -> str:
        pass

    @abstractmethod
    def load_average(self) -> str:
        pass

    @abstractmethod
    def process_count(self) -> str:
        pass
