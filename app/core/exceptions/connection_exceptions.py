class ConnectionException(Exception):
    """Base class for all remote connection failures."""


class AuthenticationException(ConnectionException):
    """Invalid credentials."""


class ConnectionTimeoutException(ConnectionException):
    """Connection timed out."""


class HostUnreachableException(ConnectionException):
    """Host cannot be reached."""


class CommandExecutionException(ConnectionException):
    """Remote command execution failed."""


class ConnectorNotSupportedException(ConnectionException):
    """Unsupported connector type."""
