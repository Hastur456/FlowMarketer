import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication.strategy import DatabaseStrategy

from app.infrastructure.db.models.user import User
from app.infrastructure.db.session import get_session
from app.modules.user.adapters.auth_adapter.backend import authentication_backend
from app.modules.user.adapters.auth_adapter.strategy import get_database_strategy


SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, reques=None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request=None):
        print(f"User {user.id} forgot password. Token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request=None):
        print(f"Verification requested for user {user.id}. Token: {token}")
