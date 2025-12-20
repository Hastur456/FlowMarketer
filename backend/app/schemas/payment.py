# backend/app/schemas/payment.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class PaymentMethod(str, Enum):
    CARD = "card"
    YANDEX_KASSA = "yandex_kassa"
    SBERBANK = "sberbank"
    QIWI = "qiwi"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentInitiateRequest(BaseModel):
    """Схема для инициации платежа"""
    
    order_id: int = Field(..., gt=0, description="ID заказа")
    method: PaymentMethod = Field(..., description="Способ оплаты")
    save_card: bool = Field(False, description="Сохранить карту")


class PaymentCallbackRequest(BaseModel):
    """Схема для callback от платёжной системы"""
    
    transaction_id: str = Field(..., description="ID транзакции")
    status: PaymentStatus = Field(..., description="Статус платежа")
    amount: Decimal = Field(..., decimal_places=2, description="Сумма")
    timestamp: datetime = Field(..., description="Время")


class PaymentResponse(BaseModel):
    """Схема ответа платежа"""
    
    id: int
    order_id: int
    method: PaymentMethod
    status: PaymentStatus
    amount: Decimal
    currency: str
    transaction_id: Optional[str]
    card_last_four: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentDetailResponse(PaymentResponse):
    """Детальная схема платежа"""
    
    receipt_number: Optional[str]
    fiscal_receipt_url: Optional[str]
    refund_amount: Decimal
    refunded_at: Optional[datetime]
    error_message: Optional[str]
    updated_at: datetime


class PaymentListResponse(BaseModel):
    """Список платежей"""
    
    total: int
    payments: List[PaymentResponse]


class RefundRequest(BaseModel):
    """Схема для возврата средств"""
    
    payment_id: int = Field(..., gt=0, description="ID платежа")
    amount: Optional[Decimal] = Field(None, gt=0, description="Сумма возврата (полный если не указано)")
    reason: str = Field(..., min_length=10, max_length=500, description="Причина возврата")


class RefundResponse(BaseModel):
    """Схема ответа возврата"""
    
    refund_id: int
    payment_id: int
    amount: Decimal
    status: str
    created_at: datetime
