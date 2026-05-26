from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.product.application.dto import ProductCreateDTO, ProductUpdateDTO


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category_id: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    discount_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    cost_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_quantity: int = Field(0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    gallery_urls: Optional[list[str]] = None
    is_featured: bool = False
    is_bestseller: bool = False

    @field_validator("discount_price")
    @classmethod
    def discount_less_than_price(cls, value, info):
        if value is not None and "price" in info.data and value >= info.data["price"]:
            raise ValueError("Discount price must be less than price")
        return value

    def to_dto(self) -> ProductCreateDTO:
        return ProductCreateDTO(**self.model_dump())


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    slug: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category_id: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    discount_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    cost_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    gallery_urls: Optional[list[str]] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_bestseller: Optional[bool] = None

    @field_validator("discount_price")
    @classmethod
    def discount_less_than_price(cls, value, info):
        if value is not None and "price" in info.data and info.data["price"] is not None:
            if value >= info.data["price"]:
                raise ValueError("Discount price must be less than price")
        return value

    def to_dto(self) -> ProductUpdateDTO:
        return ProductUpdateDTO(**self.model_dump(exclude_unset=True))


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    category_id: int
    price: Decimal
    discount_price: Optional[Decimal] = None
    stock_quantity: int
    sku: Optional[str] = None
    image_url: Optional[str] = None
    average_rating: float
    review_count: int
    is_active: bool
    is_featured: bool
    is_bestseller: bool
    created_at: datetime


class ProductDetailResponse(ProductResponse):
    description: Optional[str] = None
    cost_price: Optional[Decimal] = None
    gallery_urls: Optional[list[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: Optional[str] = None
    updated_at: datetime


class ProductListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    products: list[ProductResponse]
