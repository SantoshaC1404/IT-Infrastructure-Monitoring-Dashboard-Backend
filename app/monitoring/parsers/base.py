from abc import ABC, abstractmethod


class BaseMetricsParser(ABC):
    """
    Converts raw command outputs into Python values.

    Each OS has different command outputs, therefore every
    operating system gets its own parser implementation.
    """

    @abstractmethod
    def cpu_usage(self, output: str) -> float: ...

    @abstractmethod
    def memory_usage(self, output: str) -> float: ...

    @abstractmethod
    def disk_usage(self, output: str) -> float: ...

    @abstractmethod
    def network_usage(self, output: str) -> tuple[int, int]: ...

    @abstractmethod
    def uptime(self, output: str) -> int: ...

    @abstractmethod
    def load_average(self, output: str) -> float: ...

    @abstractmethod
    def process_count(self, output: str) -> int: ...
