import sys
from pathlib import Path
from uuid import UUID

import pytest_asyncio
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.infrastructure.db.base import Base
from app.modules.product.infrastructure.persistence.product_model import ProductModel


TEST_DATABASE_URL = "sqlite+aiosqlite://"


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products = relationship("ProductModel", back_populates="category")


class OrderItem(Base):
    __tablename__ = "order_items"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    product = relationship("ProductModel", back_populates="order_items")


class CartItem(Base):
    __tablename__ = "cart_items"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    product = relationship("ProductModel", back_populates="cart_items")


class Review(Base):
    __tablename__ = "reviews"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    product = relationship("ProductModel", back_populates="reviews")


@pytest_asyncio.fixture
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine):
    session_maker = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def category(db_session: AsyncSession) -> Category:
    category = Category(name="Test category")
    db_session.add(category)
    await db_session.flush()
    return category


@pytest_asyncio.fixture
async def product_repository(db_session: AsyncSession):
    from app.modules.product.infrastructure.persistence.sqlalchemy_product_repository import (
        SqlAlchemyProductRepository,
    )

    return SqlAlchemyProductRepository(db_session)
