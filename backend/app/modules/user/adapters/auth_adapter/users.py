from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.models.user import User, SQLAlchemyUserDatabase
from app.infrastructure.db.session import get_session


async def get_users_db(
    session: AsyncSession = Depends(get_session)
):
    yield SQLAlchemyUserDatabase(session, User)
