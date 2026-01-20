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
from app.database.session import connection, get_session


class AccessToken(Base, SQLAlchemyBaseAccessTokenTableUUID):  
    user_id: Mapped[UUID] = mapped_column(
        UUID, 
        ForeignKey("users.id", ondelete="cascade"), 
        nullable=False,
    )

    @connection()
    def get_db(
        cls,
        session: AsyncSession
    ):  
        return SQLAlchemyAccessTokenDatabase(session, AccessToken)
