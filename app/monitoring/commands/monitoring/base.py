from abc import ABC, abstractmethod


class BaseCommandSet(ABC):

    @abstractmethod
    def cpu_usage(self) -> str: ...

    @abstractmethod
    def memory_usage(self) -> str: ...

    @abstractmethod
    def disk_usage(self) -> str: ...

    @abstractmethod
    def network_usage(self) -> str: ...

    @abstractmethod
    def uptime(self) -> str: ...

    @abstractmethod
    def load_average(self) -> str: ...

    @abstractmethod
    def process_count(self) -> str: ...
