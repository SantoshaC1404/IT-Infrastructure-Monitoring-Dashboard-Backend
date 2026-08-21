from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.models.user import User
from app.schemas.auth.user import UserResponse, UserUpdate
from app.schemas.common import MessageResponse
from app.services.user.user_service import UserService
from app.utils.enums import UserRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def list_users(db: Session = Depends(get_db)):
    return UserService(db).list_users()


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Convenience alias for /auth/me, scoped under the users resource."""
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService(db).get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db),
):
    return UserService(db).update_user(user_id, request)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService(db).delete_user(user_id)
    return MessageResponse(message="User deleted successfully.")
