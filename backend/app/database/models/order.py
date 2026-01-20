from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, DateTime, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from app.database.models.base import Base


class OrderStatus(str, Enum):
    PENDING = "pending"           # Ожидание оплаты
    PAID = "paid"                 # Оплачено
    PROCESSING = "processing"     # В обработке
    SHIPPED = "shipped"           # Отправлено
    DELIVERED = "delivered"       # Доставлено
    CANCELLED = "cancelled"       # Отменено
    REFUNDED = "refunded"         # Возврат

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index('idx_orders_user_id', 'user_id'),
        Index('idx_orders_status', 'status'),
        Index('idx_orders_created_at', 'created_at'),
    )
    
    # Пользователь
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Статус
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    
    # Сумма
    subtotal = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    shipping_cost = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Адрес доставки
    shipping_address = Column(Text, nullable=False)  # JSON
    billing_address = Column(Text, nullable=True)    # JSON
    
    # Доставка
    shipping_method = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    estimated_delivery = Column(DateTime, nullable=True)
    
    # Комментарии
    customer_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    
    # Отношения
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_price})>"
