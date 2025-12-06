# backend/app/schemas/search.py

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductFilterRequest(BaseModel):
    """Схема фильтра для товаров"""
    
    query: Optional[str] = Field(None, max_length=255, description="Поисковый запрос")
    category_id: Optional[int] = Field(None, gt=0, description="ID категории")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Минимальная цена")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Максимальная цена")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Минимальный рейтинг")
    is_featured: Optional[bool] = Field(None, description="Только избранные")
    is_bestseller: Optional[bool] = Field(None, description="Только бестселлеры")
    in_stock: Optional[bool] = Field(None, description="Только в наличии")
    sort_by: Optional[str] = Field("created_at", regex=r"^(created_at|price|rating|name)$", description="Сортировка")
    sort_order: Optional[str] = Field("desc", regex=r"^(asc|desc)$", description="Порядок")
    skip: int = Field(0, ge=0, description="Пропустить")
    limit: int = Field(20, ge=1, le=100, description="Лимит")


class OrderFilterRequest(BaseModel):
    """Схема фильтра для заказов"""
    
    status: Optional[str] = Field(None, description="Статус заказа")
    date_from: Optional[str] = Field(None, description="Дата от (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="Дата до (YYYY-MM-DD)")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Минимальная сумма")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Максимальная сумма")
    sort_by: Optional[str] = Field("created_at", regex=r"^(created_at|total_price)$")
    sort_order: Optional[str] = Field("desc", regex=r"^(asc|desc)$")
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
