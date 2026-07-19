from abc import ABC, abstractmethod

from app.dto.discovery_result import DiscoveryResult


class BaseDiscovery(ABC):
    """
    Base class for all discovery implementations.
    """

    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def discover(self) -> DiscoveryResult:
        """
        Discover device inventory.
        """
        pass
