from fastapi import status


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "APPLICATION_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class DeviceAlreadyExistsException(AppException):

    def __init__(self, ip_address: str):
        super().__init__(
            message=f"Device with IP '{ip_address}' already exists.",
            status_code=status.HTTP_409_CONFLICT,
            error_code="DEVICE_ALREADY_EXISTS",
        )


class DeviceNotFoundException(AppException):

    def __init__(self, device_id: int):
        super().__init__(
            message=f"Device '{device_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="DEVICE_NOT_FOUND",
        )


class SSHAuthenticationException(AppException):

    def __init__(self):
        super().__init__(
            message="Authentication failed. Verify the SSH username and password.",
            status_code=401,
            error_code="SSH_AUTH_FAILED",
        )


class SSHTimeoutException(AppException):

    def __init__(self):
        super().__init__(
            message="Connection timed out. Verify the IP address, SSH port, and network connectivity.",
            status_code=408,
            error_code="SSH_TIMEOUT",
        )


class SSHConnectionException(AppException):

    def __init__(
        self,
        message: str = "Unable to establish SSH connection.",
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SSH_CONNECTION_FAILED",
        )


class ConnectionException(AppException):

    def __init__(
        self,
        message: str = "Unable to establish connection.",
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code="CONNECTION_FAILED",
        )


class DeviceConnectionException(AppException):

    def __init__(
        self,
        message: str = "Unable to establish SSH connection.",
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SSH_CONNECTION_FAILED",
        )


class HostUnreachableException(AppException):

    def __init__(self):
        super().__init__(
            message="Host is unreachable. Verify the IP address and ensure the device is powered on.",
            status_code=503,
            error_code="HOST_UNREACHABLE",
        )


class DatabaseException(AppException):
    def __init__(self, message: str = "A database error occurred."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_DEVICE_ERROR,
            error_code="DATABASE_ERROR",
        )


# class ResourceNotFoundException(AppException):
#     def __init__(self, message: str = "Resource not found."):
#         super().__init__(
#             message=message,
#             status_code=status.HTTP_404_NOT_FOUND,
#             error_code="RESOURCE_NOT_FOUND",
#         )
class ResourceNotFoundException(AppException):

    def __init__(self, resource: str, resource_id: int | str):

        super().__init__(
            message=f"{resource} '{resource_id}' not found.",
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class InventoryDiscoveryException(AppException):
    def __init__(self, message: str = "Inventory Discovery Error."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_DEVICE_ERROR,
            error_code="INVENTORY_DISCOVERY_ERROR",
        )
