from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth.user import UserCreate

from .login_service import LoginService
from .logout_service import LogoutService
from .register_service import RegisterService


class AuthService:
    """
    Facade over the register/login/logout services so routes have a
    single, simple entry point - mirrors the DeviceService facade
    pattern used elsewhere in this codebase.
    """

    def __init__(self, db: Session):
        self._register_service = RegisterService(db)
        self._login_service = LoginService(db)
        self._logout_service = LogoutService(db)

    def register(self, user_data: UserCreate) -> User:
        return self._register_service.register(user_data)

    def login(self, username: str, password: str) -> tuple[str, int]:
        return self._login_service.login(username, password)

    def logout(self, token: str) -> None:
        return self._logout_service.logout(token)
