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
