from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID as SA_UUID

from app.infrastructure.db.base import Base


class ProductModel(Base):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    category_id: Mapped[SA_UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    discount_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    cost_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    reserved_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    sku: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    meta_title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    meta_description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    tags: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    gallery_urls: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    average_rating: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    review_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_bestseller: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    popularity_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    sales_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<ProductModel(id={self.id}, name={self.name}, price={self.price})>"
