# backend/app/schemas/user_address.py

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserAddressCreateRequest(BaseModel):
    """Схема для создания адреса"""
    
    country: str = Field(default="Russia", description="Страна")
    region: str = Field(..., min_length=2, max_length=100, description="Регион")
    city: str = Field(..., min_length=2, max_length=100, description="Город")
    postal_code: str = Field(..., max_length=20, description="Почтовый индекс")
    street: str = Field(..., min_length=3, max_length=255, description="Улица")
    building: str = Field(..., min_length=1, max_length=50, description="Дом")
    apartment: Optional[str] = Field(None, max_length=50, description="Квартира")
    recipient_name: str = Field(..., min_length=2, max_length=255, description="Имя получателя")
    recipient_phone: str = Field(..., regex=r"^\+?[0-9\-\s\(\)]{10,}$", description="Телефон")
    is_default: bool = Field(False, description="По умолчанию")
    is_billing: bool = Field(False, description="Адрес доставки")


class UserAddressUpdateRequest(BaseModel):
    """Схема для обновления адреса"""
    
    region: Optional[str] = Field(None, min_length=2, max_length=100)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    street: Optional[str] = Field(None, min_length=3, max_length=255)
    building: Optional[str] = Field(None, min_length=1, max_length=50)
    apartment: Optional[str] = Field(None, max_length=50)
    recipient_name: Optional[str] = Field(None, min_length=2, max_length=255)
    recipient_phone: Optional[str] = Field(None, regex=r"^\+?[0-9\-\s\(\)]{10,}$")
    is_default: Optional[bool] = Field(None)
    is_billing: Optional[bool] = Field(None)


class UserAddressResponse(BaseModel):
    """Схема ответа адреса"""
    
    id: int
    country: str
    region: str
    city: str
    postal_code: str
    street: str
    building: str
    apartment: Optional[str]
    recipient_name: str
    recipient_phone: str
    is_default: bool
    is_billing: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserAddressDetailResponse(UserAddressResponse):
    """Детальная схема адреса"""
    
    updated_at: datetime
