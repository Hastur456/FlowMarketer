from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Product(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: Optional[UUID] = None
    name: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category_id: UUID

    price: Decimal = Field(..., gt=0)
    discount_price: Optional[Decimal] = Field(None, gt=0)
    cost_price: Optional[Decimal] = Field(None, gt=0)

    stock_quantity: int = Field(default=0, ge=0)
    reserved_stock: int = Field(default=0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)

    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)

    image_url: Optional[str] = Field(None, max_length=500)
    gallery_urls: Optional[list[str]] = None

    average_rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)

    is_active: bool = True
    is_featured: bool = False
    is_bestseller: bool = False

    popularity_score: int = Field(default=0, ge=0)
    sales_count: int = Field(default=0, ge=0)
    view_count: int = Field(default=0, ge=0)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name", "slug")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value

    @model_validator(mode="after")
    def validate_product_rules(self) -> "Product":
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("Discount price must be less than price")

        if self.reserved_stock > self.stock_quantity:
            raise ValueError("Reserved stock cannot exceed stock quantity")

        return self

    @property
    def available_stock(self) -> int:
        return self.stock_quantity - self.reserved_stock

    @property
    def is_available(self) -> bool:
        return self.is_active and self.available_stock > 0

    @property
    def discount_percent(self) -> float:
        if self.discount_price is None:
            return 0.0

        return (
            (float(self.price) - float(self.discount_price))
            / float(self.price)
            * 100
        )

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_price(self, price: Decimal) -> None:
        if price <= 0:
            raise ValueError("Price must be positive")

        if self.discount_price is not None and self.discount_price >= price:
            raise ValueError("Discount price must be less than price")

        self.price = price

    def set_discount_price(self, discount_price: Optional[Decimal]) -> None:
        if discount_price is not None and discount_price >= self.price:
            raise ValueError("Discount price must be less than price")

        self.discount_price = discount_price

    def increase_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.stock_quantity += quantity

    def decrease_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.available_stock < quantity:
            raise ValueError("Not enough available stock")

        self.stock_quantity -= quantity

    def reserve_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.available_stock < quantity:
            raise ValueError("Not enough available stock")

        self.reserved_stock += quantity

    def release_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.reserved_stock = max(0, self.reserved_stock - quantity)

    def register_sale(self, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.reserved_stock < quantity:
            raise ValueError("Not enough reserved stock")

        self.reserved_stock -= quantity
        self.stock_quantity -= quantity
        self.sales_count += quantity

    def register_view(self) -> None:
        self.view_count += 1
