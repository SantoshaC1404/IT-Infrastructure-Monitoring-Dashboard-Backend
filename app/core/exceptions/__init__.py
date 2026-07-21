from .base import AppException

from .connection import (
    AuthenticationException,
    CommandExecutionException,
    ConnectionException,
    ConnectionTimeoutException,
    ConnectorNotSupportedException,
    HostUnreachableException,
)

from .database import DatabaseException

from .discovery import (
    DiscoveryException,
    InventoryDiscoveryException,
    MonitoringDiscoveryException,
)

from .resources import (
    DeviceNotFoundException,
    ResourceNotFoundException,
)

from .validation import (
    DeviceAlreadyExistsException,
    ValidationException,
)

__all__ = [
    "AppException",
    "ConnectionException",
    "AuthenticationException",
    "ConnectionTimeoutException",
    "HostUnreachableException",
    "CommandExecutionException",
    "ConnectorNotSupportedException",
    "DatabaseException",
    "DiscoveryException",
    "InventoryDiscoveryException",
    "MonitoringDiscoveryException",
    "ResourceNotFoundException",
    "DeviceNotFoundException",
    "ValidationException",
    "DeviceAlreadyExistsException",
]
