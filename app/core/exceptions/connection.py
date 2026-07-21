from fastapi import status

from .base import AppException


class ConnectionException(AppException):
    """
    Generic remote connection failure.
    """

    def __init__(
        self,
        message: str = "Unable to establish connection.",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="CONNECTION_FAILED",
        )


class AuthenticationException(ConnectionException):

    def __init__(
        self,
        message: str = "Authentication failed. Verify username and password.",
    ):
        super().__init__(message)
        self.error_code = "AUTHENTICATION_FAILED"


class ConnectionTimeoutException(ConnectionException):

    def __init__(
        self,
        message: str = "Connection timed out.",
    ):
        super().__init__(message)
        self.error_code = "CONNECTION_TIMEOUT"


class HostUnreachableException(ConnectionException):

    def __init__(
        self,
        message: str = "Host is unreachable.",
    ):
        super().__init__(message)
        self.error_code = "HOST_UNREACHABLE"


class CommandExecutionException(ConnectionException):

    def __init__(
        self,
        message: str = "Remote command execution failed.",
    ):
        super().__init__(message)
        self.error_code = "COMMAND_EXECUTION_FAILED"


class ConnectorNotSupportedException(ConnectionException):

    def __init__(
        self,
        connector: str,
    ):
        super().__init__(f"{connector} connector is not supported.")
        self.error_code = "CONNECTOR_NOT_SUPPORTED"
