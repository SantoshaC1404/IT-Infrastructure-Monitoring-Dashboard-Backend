from abc import ABC, abstractmethod


class BaseDiscoveryCommandSet(ABC):

    # Server Detection
    @abstractmethod
    def detect_os(self) -> str:
        pass

    # Inventory
    @abstractmethod
    def hostname(self) -> str:
        pass

    @abstractmethod
    def operating_system(self) -> str:
        pass

    @abstractmethod
    def os_version(self) -> str:
        pass

    @abstractmethod
    def kernel_version(self) -> str:
        pass

    @abstractmethod
    def architecture(self) -> str:
        pass

    @abstractmethod
    def cpu_model(self) -> str:
        pass

    @abstractmethod
    def physical_cores(self) -> str:
        pass

    @abstractmethod
    def logical_cores(self) -> str:
        pass

    @abstractmethod
    def total_memory(self) -> str:
        pass

    @abstractmethod
    def virtualization(self) -> str:
        pass

    # Disks
    @abstractmethod
    def disk_inventory(self) -> str:
        pass

    # Network
    @abstractmethod
    def network_interfaces(self) -> str:
        pass
