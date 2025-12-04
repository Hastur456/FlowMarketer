from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.base import get_session
from pydantic import BaseModel


class BaseRepository:
    model = None

    @classmethod
    @get_session
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: str):
        request = select(cls.model).filter_by(data_id)
        
        response = await session.execute(request)
        record = response.scalar_one_or_none()

        if record is None:
            return record

        else:
            return None
