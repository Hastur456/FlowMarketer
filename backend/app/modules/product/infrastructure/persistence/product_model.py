from sqlalchemy import Boolean, Column, Float, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as SA_UUID

from app.infrastructure.db.base import Base


class ProductModel(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("idx_products_slug", "slug", unique=True),
        Index("idx_products_category_id", "category_id"),
        Index("idx_products_is_active", "is_active"),
        Index("idx_products_price", "price"),
    )

    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(SA_UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)

    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    cost_price = Column(Numeric(10, 2), nullable=True)

    stock_quantity = Column(Integer, default=0, nullable=False)
    reserved_stock = Column(Integer, default=0, nullable=False)
    sku = Column(String(100), unique=True, nullable=True, index=True)

    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)

    image_url = Column(String(500), nullable=True)
    gallery_urls = Column(Text, nullable=True)

    average_rating = Column(Float, default=0.0, nullable=False)
    review_count = Column(Integer, default=0, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_bestseller = Column(Boolean, default=False, nullable=False)

    popularity_score = Column(Integer, default=0, nullable=False)
    sales_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ProductModel(id={self.id}, name={self.name}, price={self.price})>"
