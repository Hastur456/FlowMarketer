from fastapi import APIRouter 

from app.modules.user.authentication.fastapi_users import fastapi_users
from app.infrastructure.authentication import authentication_backend
from app.core.schemas.user import (
    UserCreate, 
    UserRead, 
    UserUpdate, 
    UserRegisteredNotification
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# login/
# logout/
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)

# register 
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate
    )
)
