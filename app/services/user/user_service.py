from sqlalchemy.orm import Session

from app.core.exceptions.auth import UserNotFoundException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth.user import UserUpdate


class UserService:
    """
    Manages user *resources* (list/view/update role/deactivate/delete) -
    distinct from the authentication actions in AuthService
    (register/login/logout). Intended for admin-facing endpoints.
    """

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def list_users(self) -> list[User]:
        return self.user_repo.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException(user_id)

        return user

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(user, field, value)

        return self.user_repo.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.user_repo.delete(user)
