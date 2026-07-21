from fastapi import status

from .base import AppException


class DatabaseException(AppException):

    def __init__(
        self,
        message: str = "Database operation failed.",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
        )
