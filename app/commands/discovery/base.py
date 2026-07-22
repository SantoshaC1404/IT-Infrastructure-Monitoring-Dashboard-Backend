from abc import ABC, abstractmethod

from app.dto.command_dto import Command


class BaseDiscoveryCommandSet(ABC):

    # Server Detection
    @abstractmethod
    def detect_os(self) -> Command:
        pass

    # Inventory
    @abstractmethod
    def hostname(self) -> Command:
        pass

    @abstractmethod
    def operating_system(self) -> Command:
        pass

    @abstractmethod
    def os_version(self) -> Command:
        pass

    @abstractmethod
    def kernel_version(self) -> Command:
        pass

    @abstractmethod
    def architecture(self) -> Command:
        pass

    @abstractmethod
    def cpu_model(self) -> Command:
        pass

    @abstractmethod
    def physical_cores(self) -> Command:
        pass

    @abstractmethod
    def logical_cores(self) -> Command:
        pass

    @abstractmethod
    def total_memory(self) -> Command:
        pass

    @abstractmethod
    def virtualization(self) -> Command:
        pass

    # Disks
    @abstractmethod
    def disk_inventory(self) -> Command:
        pass

    # Network
    @abstractmethod
    def network_interfaces(self) -> Command:
        pass
