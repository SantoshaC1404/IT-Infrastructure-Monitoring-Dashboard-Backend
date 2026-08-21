from sqlalchemy.orm import Session

from app.core.exceptions.auth import UserAlreadyExistsException
from app.core.security.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth.user import UserCreate


class RegisterService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> User:

        if self.user_repo.get_by_email(user_data.email):
            raise UserAlreadyExistsException("email", user_data.email)

        if self.user_repo.get_by_username(user_data.username):
            raise UserAlreadyExistsException("username", user_data.username)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            role=user_data.role,
        )

        return self.user_repo.create(user)
