from fastapi import APIRouter 

from app.modules.auth.authentication.fastapi_users import fastapi_users
from app.modules.auth.adapters.auth_adapter import authentication_backend
from app.modules.auth.schemas import (
    UserCreate,
    UserRead
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

