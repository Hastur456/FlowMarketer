from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as SA_UUID
from app.database.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        Index('idx_order_items_order_id', 'order_id'),
        Index('idx_order_items_product_id', 'product_id'),
    )
    
    order_id = Column(SA_UUID, ForeignKey('orders.id'), nullable=False)
    product_id = Column(SA_UUID, ForeignKey('products.id'), nullable=False)
    
    # Информация о товаре в момент заказа
    product_name = Column(String(255), nullable=False)
    product_sku = Column(String(100), nullable=True)
    
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # Цена товара на момент заказа
    discount = Column(Numeric(10, 2), default=0)
    subtotal = Column(Numeric(10, 2), nullable=False)  # quantity * price - discount
    
    # Отношения
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"
