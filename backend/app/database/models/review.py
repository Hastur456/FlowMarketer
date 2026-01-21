from sqlalchemy import Column, String, Integer, ForeignKey, Text, Index, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as SA_UUID
from app.database.models.base import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        Index('idx_reviews_product_id', 'product_id'),
        Index('idx_reviews_user_id', 'user_id'),
    )
    
    product_id = Column(SA_UUID, ForeignKey('products.id'), nullable=False)
    user_id = Column(SA_UUID, ForeignKey('users.id'), nullable=False)
    
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    
    is_verified_purchase = Column(Boolean, default=False)
    
    # Отношения
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(product_id={self.product_id}, user_id={self.user_id}, rating={self.rating})>"
