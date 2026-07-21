from fastapi import status

from .base import AppException


class DiscoveryException(AppException):

    def __init__(
        self,
        message: str = "Device discovery failed.",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DISCOVERY_FAILED",
        )


class InventoryDiscoveryException(DiscoveryException):

    def __init__(
        self,
        message: str = "Failed to collect device inventory.",
    ):
        super().__init__(message)
        self.error_code = "INVENTORY_DISCOVERY_FAILED"


class MonitoringDiscoveryException(DiscoveryException):

    def __init__(
        self,
        message: str = "Failed to collect monitoring data.",
    ):
        super().__init__(message)
        self.error_code = "MONITORING_DISCOVERY_FAILED"
