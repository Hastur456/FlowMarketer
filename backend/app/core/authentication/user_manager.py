import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.database.models.user import User
from app.database.session import get_session

SECRET = "SECRET"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request=None):
        print(f"User {user.id} forgot password. Token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request=None):
        print(f"Verification requested for user {user.id}. Token: {token}")
