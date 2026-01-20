from sqlalchemy import Column, String, Text, Boolean, Index, Integer
from sqlalchemy.orm import relationship
from app.database.models.base import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        Index('idx_categories_slug', 'slug', unique=True),
        Index('idx_categories_is_active', 'is_active'),
    )
    
    name = Column(String(200), nullable=False, unique=True, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
