from fastapi import Depends, BackgroundTasks

from .users import get_users_db
from app.modules.user.authentication.user_manager import UserManager
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
        user_db = Depends(get_users_db),
):
    yield UserManager(
        user_db
    )
