from fastapi import status

from .base import AppException


class InvalidCredentialsException(AppException):

    def __init__(self):
        super().__init__(
            message="Invalid username or password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS",
        )


class InactiveUserException(AppException):

    def __init__(self):
        super().__init__(
            message="This account has been deactivated.",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="INACTIVE_USER",
        )


class InvalidTokenException(AppException):

    def __init__(self, message: str = "Invalid or expired token."):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN",
        )


class InsufficientPermissionsException(AppException):

    def __init__(self):
        super().__init__(
            message="You do not have permission to perform this action.",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="INSUFFICIENT_PERMISSIONS",
        )


class UserAlreadyExistsException(AppException):

    def __init__(self, field: str, value: str):
        super().__init__(
            message=f"A user with this {field} already exists.",
            status_code=status.HTTP_409_CONFLICT,
            error_code="USER_ALREADY_EXISTS",
        )
        self.field = field
        self.value = value


class UserNotFoundException(AppException):

    def __init__(self, user_id: int):
        super().__init__(
            message=f"User '{user_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="USER_NOT_FOUND",
        )
