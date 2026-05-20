import uuid
from typing import TYPE_CHECKING
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication.strategy import DatabaseStrategy

from app.modules.user.models.user import User
from app.infrastructure.db.session import get_session
from app.modules.auth.adapters.auth_adapter.backend import authentication_backend
from app.modules.auth.adapters.auth_adapter.strategy import get_database_strategy

if TYPE_CHECKING:
    from fastapi import Request, BackgroundTasks
    from fastapi_users.password import PasswordHelperProtocol

from app.core.config import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.auth.SECRET
    verification_token_secret = settings.auth.SECRET

    async def on_after_register(self, user: User, reques=None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request=None):
        print(f"User {user.id} forgot password. Token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request=None):
        print(f"Verification requested for user {user.id}. Token: {token}")
