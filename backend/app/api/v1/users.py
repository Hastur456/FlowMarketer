from fastapi import APIRouter 

from app.modules.user.authentication.fastapi_users import fastapi_users
from app.modules.user.adapters.auth_adapter import authentication_backend
from app.modules.user.schemas import (
    UserCreate, 
    UserRead, 
    UserUpdate, 
    UserRegisteredNotification
)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# /me
# /{id}
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
        requires_verification=False
    )
)
