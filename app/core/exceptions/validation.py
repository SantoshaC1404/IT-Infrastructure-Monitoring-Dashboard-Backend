from fastapi import status

from .base import AppException


class ValidationException(AppException):

    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
        )


class DeviceAlreadyExistsException(ValidationException):

    def __init__(
        self,
        ip_address: str,
    ):
        super().__init__(
            message=f"Device with IP '{ip_address}' already exists.",
            error_code="DEVICE_ALREADY_EXISTS",
        )
