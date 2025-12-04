from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, TIMESTAMP, String, Integer
from uuid import uuid4
from datetime import datetime

from database.session import session_maker


def get_session(method): 
    async def wrapper(*args, **kwards):
        async with session_maker() as session:
            try:
                return await method(*args, session=session, **kwards)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper
