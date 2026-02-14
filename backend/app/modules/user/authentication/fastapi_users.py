from fastapi import Depends
from fastapi_users import FastAPIUsers
from uuid import UUID

from app.modules.user.adapters.auth_adapter import get_user_manager, authentication_backend
from app.modules.user.adapters.auth_adapter.users import User


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager=get_user_manager,
    auth_backends=[authentication_backend]
)
