from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import (
    UUID,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase, 
    mapped_column
)
from .base import Base
from database.session import connection



class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):  
    user_id: Mapped[UUID] = mapped_column(
        UUID, 
        ForeignKey("users.id", ondelete="cascade"), 
        nullable=False,
    )


@connection(commit=False)
async def get_access_token_db(
    session: AsyncSession
):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
