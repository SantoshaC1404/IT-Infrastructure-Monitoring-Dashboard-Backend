from .base import AppException

from .auth import (
    InactiveUserException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
)

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
    "InvalidCredentialsException",
    "InactiveUserException",
    "InvalidTokenException",
    "InsufficientPermissionsException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
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
