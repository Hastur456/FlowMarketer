from fastapi import APIRouter 

from app.modules.auth.authentication import fastapi_users
from app.modules.auth.schemas import (
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
