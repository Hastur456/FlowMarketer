"""Маппер для преобразования Product (ORM/dict) в ES документ"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Mapping, Optional, Union

from pydantic import BaseModel, Field, ConfigDict


Number = Union[int, float, Decimal]


class ProductSource(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: int
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    
    price: Number
    discount_price: Optional[Number] = None
    
    stock_quantity: int = 0  # ← ОТ БД (stock_quantity)
    
    category_id: int
    category_name: str
    
    average_rating: float = 0.0  # ← ОТ БД (average_rating, WAS: rating)
    review_count: int = 0
    
    is_active: bool = True
    is_featured: bool = False
    is_bestseller: bool = False
    
    popularity_score: int = 0  # ← ОТ БД (новое поле)
    sales_count: int = 0       # ← ОТ БД (новое поле)
    view_count: int = 0        # ← ОТ БД (новое поле)
    
    created_at: datetime
    updated_at: datetime


class ProductESDocument(BaseModel):
    """
    Документ в ES.
    ТОЧНО соответствует ProductIndexConfig.MAPPINGS
    """
    model_config = ConfigDict(extra="ignore")
    
    id: int
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    search_text: str
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int
    is_available: bool
    is_active: bool
    is_featured: bool
    is_bestseller: bool
    category_id: int
    category_name: str
    average_rating: float
    review_count: int
    popularity_score: int
    sales_count: int
    view_count: int
    created_at: datetime
    updated_at: datetime


class ProductMapper:
    """Маппер товаров."""
    
    @staticmethod
    def _normalize_text(value: Optional[str]) -> str:
        if not value:
            return ""
        return " ".join(value.lower().split())
    
    @classmethod
    def _build_search_text(cls, p: ProductSource) -> str:
        """Построить поисковый текст из нескольких полей."""
        parts = [
            cls._normalize_text(p.name),
            cls._normalize_text(p.description),
            cls._normalize_text(p.sku),
            cls._normalize_text(p.category_name),
        ]
        return " ".join([x for x in parts if x])
    
    @classmethod
    def to_es_document(cls, source: Union[ProductSource, Mapping[str, Any]]) -> Dict[str, Any]:
        """
        Преобразование Product (ORM/dict) в ES документ.
        КАЛИБРОВАНО под ProductIndexConfig.MAPPINGS
        """
        p = source if isinstance(source, ProductSource) else ProductSource.model_validate(source)
        
        # is_available вычисляется: is_active AND stock_quantity > 0
        is_available = bool(p.is_active and p.stock_quantity > 0)
        
        return {
            "id": p.id,
            "sku": p.sku,
            "name": p.name,
            "description": p.description,
            "search_text": cls._build_search_text(p),
            "price": float(p.price),
            "discount_price": float(p.discount_price) if p.discount_price else None,
            "stock_quantity": p.stock_quantity,  # ← FROM: stock_quantity (НЕ stock)
            "is_available": is_available,
            "is_active": p.is_active,
            "is_featured": p.is_featured,
            "is_bestseller": p.is_bestseller,
            "category_id": p.category_id,
            "category_name": p.category_name,
            "average_rating": float(p.average_rating),  # ← FROM: average_rating (НЕ rating)
            "review_count": p.review_count,
            "popularity_score": p.popularity_score,  # ← НОВОЕ
            "sales_count": p.sales_count,            # ← НОВОЕ
            "view_count": p.view_count,              # ← НОВОЕ
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
        }
        
    @classmethod
    def from_es_hit(cls, hit: Mapping[str, Any]) -> ProductESDocument:
        """Преобразование ES hit в типизированную модель."""
        source = hit.get("_source") or {}
        return ProductESDocument.model_validate(source)
