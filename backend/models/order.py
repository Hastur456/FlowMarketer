from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import ENUM  
from enum import StrEnum
from backend.app.infrastructure.db.base import Base


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index('idx_orders_user_id', 'user_id'),
        Index('idx_orders_status', 'status'),
        Index('idx_orders_created_at', 'created_at'),
    )

    user_id = Column(SA_UUID, ForeignKey('users.id'), nullable=False)

    status = Column(
        ENUM(
            OrderStatus,
            name="orderstatus",
            create_type=False  
        ),
        nullable=False,
        default=OrderStatus.PENDING
    )

    subtotal = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0)
    shipping_cost = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    total_price = Column(Numeric(10, 2), nullable=False)

    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=True)
    shipping_method = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    estimated_delivery = Column(DateTime, nullable=True)

    customer_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_price})>"
