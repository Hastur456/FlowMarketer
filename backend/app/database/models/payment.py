from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, DateTime, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from app.database.models.base import Base


class PaymentMethod(str, Enum):
    CARD = "card"                 # Карта (Yandex.Kassa, etc)
    YANDEX_KASSA = "yandex_kassa" # Яндекс.Касса
    SBERBANK = "sberbank"         # СберБанк онлайн
    QIWI = "qiwi"                 # QIWI
    PAYPAL = "paypal"             # PayPal (если работают с миром)
    BANK_TRANSFER = "bank_transfer" # Банковский переводы
    INVOICE = "invoice"           # Счёт для физ.лиц

class PaymentStatus(str, Enum):
    PENDING = "pending"           # Ожидание
    PROCESSING = "processing"     # В обработке
    COMPLETED = "completed"       # Завершено
    FAILED = "failed"             # Ошибка
    CANCELLED = "cancelled"       # Отменено
    REFUNDED = "refunded"         # Возвращено

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        Index('idx_payments_order_id', 'order_id'),
        Index('idx_payments_user_id', 'user_id'),
        Index('idx_payments_status', 'status'),
        Index('idx_payments_created_at', 'created_at'),
    )
    
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Метод и статус
    method = Column(SQLEnum(PaymentMethod), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Сумма
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='RUB', nullable=False)
    
    # ID платежа в платёжной системе
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)
    receipt_number = Column(String(255), nullable=True)  # Номер чека
    
    # 3D Secure и доп. информация
    card_last_four = Column(String(4), nullable=True)
    card_brand = Column(String(50), nullable=True)  # Visa, MasterCard и т.д.
    
    # Фискальные данные (для России)
    fiscal_receipt_id = Column(String(255), nullable=True)
    fiscal_receipt_url = Column(String(500), nullable=True)
    
    # Возврат
    refund_amount = Column(Numeric(10, 2), default=0)
    refunded_at = Column(DateTime, nullable=True)
    
    # Ошибка (если статус FAILED)
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    
    # Дополнительная информация
    metadata = Column(Text, nullable=True)  # JSON
    
    # Отношения
    order = relationship("Order", back_populates="payment")
    user = relationship("User", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status={self.status}, amount={self.amount})>"
