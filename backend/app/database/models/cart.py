from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.models.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        Index('idx_cart_items_user_id', 'user_id'),
        Index('idx_cart_items_product_id', 'product_id'),
        Index('idx_cart_items_user_product', 'user_id', 'product_id', unique=True),
    )
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    
    # Отношения
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    
    def __repr__(self):
        return f"<CartItem(user_id={self.user_id}, product_id={self.product_id}, qty={self.quantity})>"
