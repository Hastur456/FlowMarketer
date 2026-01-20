from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.core.authentication.user_manager import UserManager
from app.database.session import get_session
from app.database.models.user import SQLAlchemyUserDatabase


async def get_users_db(
    session: AsyncSession = Depends(get_session)
):
    yield SQLAlchemyUserDatabase(session, User)
