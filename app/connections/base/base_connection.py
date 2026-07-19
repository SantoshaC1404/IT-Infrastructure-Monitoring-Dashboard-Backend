from __future__ import annotations

from abc import ABC, abstractmethod


class BaseConnection(ABC):
    """
    Abstract base class for all device connections.

    Supported implementations:

    - SSH
    - WinRM
    - SNMP
    - REST
    - Redfish
    """

    @abstractmethod
    def connect(self) -> None:
        """Open the connection."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, command: str) -> str:
        """
        Execute a command on the remote device.

        Returns:
            Command output as string.
        """
        raise NotImplementedError
