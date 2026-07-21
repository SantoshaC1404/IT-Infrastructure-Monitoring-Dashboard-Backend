from sqlalchemy.orm import Session

from app.core.security.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate):

        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            role=user_data.role,
        )

        return self.user_repo.create(user)

    def login(self, username: str, password: str):

        user = self.user_repo.get_by_username(username)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        token = create_access_token(
            subject=user.username,
        )

        return token
