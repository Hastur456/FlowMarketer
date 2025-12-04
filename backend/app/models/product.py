from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, Index, Float
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index('idx_products_slug', 'slug', unique=True),
        Index('idx_products_category_id', 'category_id'),
        Index('idx_products_is_active', 'is_active'),
        Index('idx_products_price', 'price'),
    )
    
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    cost_price = Column(Numeric(10, 2), nullable=True)  # Себестоимость
    
    # Остаток
    stock = Column(Integer, default=0, nullable=False)
    reserved_stock = Column(Integer, default=0)  # Зарезервировано в заказах
    sku = Column(String(100), unique=True, nullable=True, index=True)
    
    # SEO и контент
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)  # JSON как строка или отдельная таблица
    
    # Изображения
    image_url = Column(String(500), nullable=True)
    gallery_urls = Column(Text, nullable=True)  # JSON
    
    # Рейтинг
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    # Статусы
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    is_bestseller = Column(Boolean, default=False)
    
    # Отношения
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
    
    @property
    def available_stock(self):
        """Доступный остаток"""
        return self.stock - self.reserved_stock
    
    @property
    def discount_percent(self):
        """Процент скидки"""
        if self.discount_price:
            return ((float(self.price) - float(self.discount_price)) / float(self.price)) * 100
        return 0