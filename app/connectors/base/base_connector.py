from abc import ABC, abstractmethod

from app.dto.command_dto import Command


class BaseConnector(ABC):
    """
    Base interface for all device connectors.

    Every connector (SSH, WinRM, SNMP, REST, etc.)
    must implement the same contract.
    """

    @abstractmethod
    def connect(self) -> None:
        """Open the connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection."""
        pass

    @abstractmethod
    def execute(self, command: Command) -> str:
        """Execute a command and return stdout."""
        pass

    # Optional feature
    def execute_powershell(self, command):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support PowerShell."
        )

    @abstractmethod
    def execute_with_status(self, command: str) -> tuple[int, str, str]:
        """Execute a command and return (exit_code, stdout, stderr)."""
        pass

    # Context manager
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
