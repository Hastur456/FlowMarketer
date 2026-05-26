from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductCreateDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    slug: str
    description: Optional[str] = None
    category_id: int
    price: Decimal
    discount_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    stock_quantity: int = 0
    sku: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    gallery_urls: Optional[list[str]] = None
    is_featured: bool = False
    is_bestseller: bool = False


class ProductUpdateDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[Decimal] = None
    discount_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    sku: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    gallery_urls: Optional[list[str]] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_bestseller: Optional[bool] = None


class ProductSearchDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    query: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: bool = True
    limit: int = 10
    offset: int = 0
