from sqlalchemy import (
    Column, String, Numeric, ForeignKey, DateTime, Text, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID as SA_UUID
from sqlalchemy.dialects.postgresql import ENUM
from enum import StrEnum
from app.database.models.base import Base


class PaymentMethod(StrEnum):
    CARD = "card"
    YANDEX_KASSA = "yandex_kassa"
    SBERBANK = "sberbank"
    QIWI = "qiwi"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    INVOICE = "invoice"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        Index('idx_payments_order_id', 'order_id'),
        Index('idx_payments_user_id', 'user_id'),
        Index('idx_payments_status', 'status'),
        Index('idx_payments_created_at', 'created_at'),
    )

    order_id = Column(
        SA_UUID,
        ForeignKey('orders.id'),
        nullable=False,
        unique=True
    )
    user_id = Column(SA_UUID, ForeignKey('users.id'), nullable=False)

    # ENUM WITHOUT creating type in models
    method = Column(
        ENUM(
            *[m.value for m in PaymentMethod],
            name="paymentmethod",
            create_type=False,
            drop_type=False
        ),
        nullable=False
    )

    status = Column(
        ENUM(
            *[s.value for s in PaymentStatus],
            name="paymentstatus",
            create_type=False,
            drop_type=False
        ),
        nullable=False,
        default=PaymentStatus.PENDING
    )

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="RUB")

    transaction_id = Column(String(255), unique=True, index=True)
    receipt_number = Column(String(255))

    card_last_four = Column(String(4))
    card_brand = Column(String(50))

    fiscal_receipt_id = Column(String(255))
    fiscal_receipt_url = Column(String(500))

    refund_amount = Column(Numeric(10, 2), default=0)
    refunded_at = Column(DateTime)

    error_message = Column(Text)
    error_code = Column(String(50))

    payment_metadata = Column(Text)

    order = relationship("Order", back_populates="payment")
    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return (
            f"<Payment(id={self.id}, order_id={self.order_id}, "
            f"status={self.status}, amount={self.amount})>"
        )
