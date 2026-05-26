from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Mapping, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict


Number = Union[int, float, Decimal]


class ProductSource(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID | str
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None

    price: Number
    discount_price: Optional[Number] = None

    stock_quantity: int = 0

    category_id: UUID | str
    category_name: str = ""

    average_rating: float = 0.0
    review_count: int = 0

    is_active: bool = True
    is_featured: bool = False
    is_bestseller: bool = False

    popularity_score: int = 0
    sales_count: int = 0
    view_count: int = 0

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductESDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
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
    category_id: str
    category_name: str = ""
    average_rating: float
    review_count: int
    popularity_score: int
    sales_count: int
    view_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductMapper:
    @staticmethod
    def _normalize_text(value: Optional[str]) -> str:
        if not value:
            return ""
        return " ".join(value.lower().split())

    @classmethod
    def _build_search_text(cls, product: ProductSource) -> str:
        parts = [
            cls._normalize_text(product.name),
            cls._normalize_text(product.description),
            cls._normalize_text(product.sku),
            cls._normalize_text(product.category_name),
        ]
        return " ".join(part for part in parts if part)

    @classmethod
    def to_es_document(cls, source: ProductSource | Mapping[str, Any]) -> dict[str, Any]:
        product = source if isinstance(source, ProductSource) else ProductSource.model_validate(source)

        return {
            "id": str(product.id),
            "sku": product.sku,
            "name": product.name,
            "description": product.description,
            "search_text": cls._build_search_text(product),
            "price": float(product.price),
            "discount_price": float(product.discount_price) if product.discount_price else None,
            "stock_quantity": product.stock_quantity,
            "is_available": bool(product.is_active and product.stock_quantity > 0),
            "is_active": product.is_active,
            "is_featured": product.is_featured,
            "is_bestseller": product.is_bestseller,
            "category_id": str(product.category_id),
            "category_name": product.category_name,
            "average_rating": float(product.average_rating),
            "review_count": product.review_count,
            "popularity_score": product.popularity_score,
            "sales_count": product.sales_count,
            "view_count": product.view_count,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
        }

    @classmethod
    def from_es_hit(cls, hit: Mapping[str, Any]) -> ProductESDocument:
        source = hit.get("_source") or {}
        return ProductESDocument.model_validate(source)
