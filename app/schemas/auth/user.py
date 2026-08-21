from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.enums import UserRole


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Payload for self-registration (POST /auth/register)."""

    password: str = Field(..., min_length=8, max_length=255)
    role: UserRole = UserRole.VIEWER


class UserUpdate(BaseModel):
    """Payload for admin user management (PATCH /users/{id})."""

    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
