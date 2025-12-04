# backend/app/schemas/order.py

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class AddressData(BaseModel):
    """Данные адреса"""
    
    country: str = Field(default="Russia", description="Страна")
    region: str = Field(..., min_length=2, max_length=100, description="Регион/область")
    city: str = Field(..., min_length=2, max_length=100, description="Город")
    postal_code: str = Field(..., max_length=20, description="Почтовый индекс")
    street: str = Field(..., min_length=3, max_length=255, description="Улица")
    building: str = Field(..., min_length=1, max_length=50, description="Дом")
    apartment: Optional[str] = Field(None, max_length=50, description="Квартира")
    recipient_name: str = Field(..., min_length=2, max_length=255, description="Имя получателя")
    recipient_phone: str = Field(..., regex=r"^\+?[0-9\-\s\(\)]{10,}$", description="Телефон")


class OrderItemData(BaseModel):
    """Данные товара в заказе"""
    
    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(..., gt=0, description="Количество")


class OrderCreateRequest(BaseModel):
    """Схема для создания заказа"""
    
    items: List[OrderItemData] = Field(..., min_items=1, description="Товары в заказе")
    shipping_address: AddressData = Field(..., description="Адрес доставки")
    billing_address: Optional[AddressData] = Field(None, description="Адрес биллинга")
    shipping_method: str = Field(..., description="Способ доставки")
    customer_notes: Optional[str] = Field(None, max_length=1000, description="Комментарий")
    
    @validator('items')
    def items_unique(cls, v):
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError('Дублированные товары в заказе')
        return v


class OrderUpdateRequest(BaseModel):
    """Схема для обновления заказа"""
    
    customer_notes: Optional[str] = Field(None, max_length=1000)


class OrderItemResponse(BaseModel):
    """Схема ответа товара в заказе"""
    
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: Decimal
    discount: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Схема ответа заказа"""
    
    id: int
    user_id: int
    status: OrderStatus
    subtotal: Decimal
    discount_amount: Decimal
    shipping_cost: Decimal
    tax_amount: Decimal
    total_price: Decimal
    tracking_number: Optional[str]
    estimated_delivery: Optional[datetime]
    customer_notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    """Детальная схема заказа"""
    
    items: List[OrderItemResponse]
    shipping_address: dict
    billing_address: Optional[dict]
    shipping_method: str
    admin_notes: Optional[str]
    updated_at: datetime


class OrderListResponse(BaseModel):
    """Список заказов"""
    
    total: int
    skip: int
    limit: int
    orders: List[OrderResponse]


class OrderStatusUpdateRequest(BaseModel):
    """Схема для обновления статуса заказа"""
    
    status: OrderStatus = Field(..., description="Новый статус")
    admin_notes: Optional[str] = Field(None, max_length=1000, description="Примечание администратора")


class OrderCancelRequest(BaseModel):
    """Схема для отмены заказа"""
    
    reason: str = Field(..., min_length=10, max_length=500, description="Причина отмены")
