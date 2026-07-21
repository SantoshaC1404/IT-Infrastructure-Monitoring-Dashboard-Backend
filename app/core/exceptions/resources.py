from fastapi import status

from .base import AppException


class ResourceNotFoundException(AppException):

    def __init__(
        self,
        resource: str,
        resource_id: int | str,
    ):
        super().__init__(
            message=f"{resource} '{resource_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
        )


class DeviceNotFoundException(ResourceNotFoundException):

    def __init__(
        self,
        device_id: int,
    ):
        super().__init__(
            "Device",
            device_id,
        )
