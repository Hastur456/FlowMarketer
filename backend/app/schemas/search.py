from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from typing import List


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


class ProductSearchBase(BaseModel):
    """Базовая схема для поиска продуктов"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    price: float = Field(..., gt=0)
    category_id: int
    category_name: str
    sku: str
    stock_quantity: int = Field(default=0, ge=0)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    review_count: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    status: str = "active"
    
    # Для полнотекстового поиска
    search_text: Optional[str] = None

class ProductSearchDocument(ProductSearchBase):
    """Документ для Elasticsearch"""
    model_config = ConfigDict(from_attributes=True)
    
    # Дополнительные поля для ES
    brand: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    popularity_score: float = Field(default=0.0, ge=0.0)

class SearchQuery(BaseModel):
    """Запрос поиска продуктов"""
    query: str = Field(..., min_length=1, max_length=1000)
    category_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    in_stock: bool = True
    sort_by: str = Field("relevance", regex="^(relevance|price_asc|price_desc|rating|newest)$")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class SearchResult(BaseModel):
    """Результат поиска"""
    total: int
    page: int
    page_size: int
    total_pages: int
    results: List[ProductSearchDocument]
    aggregations: Optional[dict] = None
    took_ms: int  # Время выполнения

class AutocompleteQuery(BaseModel):
    """Запрос автодополнения"""
    prefix: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(10, ge=1, le=50)
    category_id: Optional[int] = None

class AutocompleteResult(BaseModel):
    """Результат автодополнения"""
    suggestions: List[str]
    took_ms: int
