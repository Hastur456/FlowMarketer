from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from decimal import Decimal


class CartItemAddRequest(BaseModel):
    """Схема для добавления товара в корзину"""
    
    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(1, gt=0, le=999, description="Количество")
    
    @model_validator('quantity')
    def quantity_valid(cls, v):
        if v > 999:
            raise ValueError('Максимум 999 штук одного товара')
        return v


class CartItemUpdateRequest(BaseModel):
    """Схема для обновления товара в корзине"""
    
    quantity: int = Field(..., gt=0, le=999, description="Новое количество")


class CartItemResponse(BaseModel):
    """Схема ответа товара в корзине"""
    
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str]
    quantity: int
    price: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Схема корзины"""
    
    items: List[CartItemResponse]
    total_items: int
    subtotal: Decimal
    discount_amount: Decimal = 0
    shipping_cost: Decimal = 0
    total_price: Decimal
    
    class Config:
        from_attributes = True
