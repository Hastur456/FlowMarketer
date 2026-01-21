from sqlalchemy import Column, String, Boolean, DateTime, Index, Text
from sqlalchemy import (
    select
)
from sqlalchemy.orm import (relationship,
    Mapped, 
    mapped_column)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from datetime import datetime
from uuid import UUID
from app.database.models.base import Base
from app.database.session import get_session
from app.database.models.access_token import AccessToken
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from typing import List

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase as SQLAlchemyUserDatabaseGeneric
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_users_email', 'email', unique=True),
        Index('idx_users_is_active', 'is_active'),
    )
    
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    phone = Column(String(20), nullable=True)
    
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    email_verified_at = Column(DateTime, nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    preferred_language = Column(String(10), default='ru')
    
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    
    access_tokens: Mapped[List[AccessToken]] = relationship(
        "AccessToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    # audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_admin={self.is_admin})>"


class IdUUIDMixin(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True)


class SQLAlchemyUserDatabase(SQLAlchemyUserDatabaseGeneric):
    async def get_users(self) -> List[User]:
        statement = select(User).order_by(User.id)
        result = await self.session.scalars(statement)
        return list(result.all())
