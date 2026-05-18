from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from .schemas import User
from .storage import RoomManager, Storage

storage = Storage()
room_manager = RoomManager()


def get_current_user(
    x_user_id: Optional[str] = Header(None),
    x_user_role: Optional[str] = Header("user"),
) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-User-Id header required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-User-Id must be int")

    return User(id=user_id, role=x_user_role or "user")


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


def get_storage() -> Storage:
    return storage


def get_room_manager() -> RoomManager:
    return room_manager
