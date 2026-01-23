from fastapi import APIRouter 

from app.core.authentication.fastapi_users import fastapi_users
from app.dependencies.authentication import authentication_backend
from app.core.schemas.user import (
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