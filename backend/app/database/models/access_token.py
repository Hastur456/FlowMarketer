from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase, 
    mapped_column,
    relationship
)
from sqlalchemy.types import UUID as SA_UUID
from app.database.models.base import Base
from uuid import UUID


class AccessToken(Base, SQLAlchemyBaseAccessTokenTableUUID):  
    __table_args__ = {'extend_existing': True}

    user_id: Mapped[UUID] = mapped_column(
        SA_UUID, 
        ForeignKey("users.id", ondelete="cascade"), 
        nullable=False,
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="access_tokens"
    )

    @classmethod
    def get_db(
        cls,
        session: AsyncSession
    ):  
        return SQLAlchemyAccessTokenDatabase(session, AccessToken)
