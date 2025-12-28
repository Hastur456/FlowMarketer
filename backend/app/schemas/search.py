from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class SearchQuery(BaseModel):
    """Параметры для поиска товаров"""
    
    query: Optional[str] = Field(
        None,
        min_length=1,
        max_length=1000,
        description="Поисковый запрос"
    )
    category_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID категории"
    )
    min_price: Optional[float] = Field(
        None,
        ge=0,
        description="Минимальная цена"
    )
    max_price: Optional[float] = Field(
        None,
        ge=0,
        description="Максимальная цена"
    )
    min_rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Минимальный рейтинг"
    )
    in_stock: bool = Field(
        True,
        description="Только товары в наличии"
    )
    sort_by: str = Field(
        "relevance",
        description="Метод сортировки"
    )
    page: int = Field(
        1,
        ge=1,
        description="Номер страницы"
    )
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Размер страницы"
    )
    
    @field_validator("sort_by")
    @classmethod
    def validate_sort_by(cls, v: str) -> str:
        """Валидация параметра сортировки"""
        allowed_sorts = {
            "relevance", "price_asc", "price_desc",
            "rating", "newest", "popular"
        }
        if v not in allowed_sorts:
            raise ValueError(f"sort_by must be one of {allowed_sorts}")
        return v
    
    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v: float, info) -> float:
        """Валидация максимальной цены"""
        if v is not None and info.data.get("min_price"):
            if v < info.data.get("min_price"):
                raise ValueError("max_price must be >= min_price")
        return v


class ProductSearchDocument(BaseModel):
    """
    Документ товара из Elasticsearch.
    СТРОГО соответствует ProductIndexConfig.MAPPINGS
    """
    
    id: int
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int  # ← WAS: stock (ИСПРАВЛЕНО)
    sku: Optional[str] = None
    category_id: int
    category_name: str
    average_rating: float = Field(ge=0.0, le=5.0)  # ← WAS: rating (ИСПРАВЛЕНО)
    review_count: int = Field(ge=0)
    is_active: bool
    is_available: bool  # ← ДОБАВЛЕНО (вычисляется из is_active + stock_quantity)
    is_featured: bool
    is_bestseller: bool
    created_at: datetime
    updated_at: datetime
    search_text: str
    popularity_score: int = Field(ge=0)  # ← ДОБАВЛЕНО
    sales_count: int = Field(ge=0)       # ← ДОБАВЛЕНО
    view_count: int = Field(ge=0)        # ← ДОБАВЛЕНО


class SearchResult(BaseModel):
    """Результат поиска с метаданными"""
    
    total: int = Field(ge=0, description="Общее количество результатов")
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(ge=1, description="Размер страницы")
    total_pages: int = Field(ge=0, description="Всего страниц")
    results: List[ProductSearchDocument] = Field(
        default_factory=list,
        description="Список товаров"
    )
    aggregations: Optional[Dict[str, Any]] = Field(
        None,
        description="Агрегации (фасеты)"
    )
    took_ms: int = Field(ge=0, description="Время выполнения в миллисекундах")


class AutocompleteQuery(BaseModel):
    """Запрос для автодополнения"""
    
    prefix: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Префикс для автодополнения"
    )
    limit: int = Field(
        10,
        ge=1,
        le=50,
        description="Максимальное количество подсказок"
    )
    category_id: Optional[int] = Field(
        None,
        gt=0,
        description="Ограничить поиск категорией"
    )


class AutocompleteResult(BaseModel):
    """Результат автодополнения"""
    
    suggestions: List[str] = Field(
        default_factory=list,
        description="Список подсказок"
    )
    took_ms: int = Field(
        default=0,
        ge=0,
        description="Время выполнения в миллисекундах"
    )
