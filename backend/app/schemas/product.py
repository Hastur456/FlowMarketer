from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ProductCreateRequest(BaseModel):
    """Схема для создания товара"""
    
    name: str = Field(..., min_length=3, max_length=255, description="Название товара")
    slug: str = Field(..., min_length=3, max_length=255, description="URL slug")
    description: Optional[str] = Field(None, max_length=5000, description="Описание")
    category_id: int = Field(..., gt=0, description="ID категории")
    
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Цена")
    discount_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2, description="Цена со скидкой")
    cost_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2, description="Себестоимость")
    
    stock_quantity: int = Field(0, ge=0, description="Остаток товара")  # ← WAS: stock (ИСПРАВЛЕНО)
    sku: Optional[str] = Field(None, max_length=100, description="SKU товара")
    
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    
    image_url: Optional[str] = Field(None, max_length=500, description="URL главной картинки")
    gallery_urls: Optional[List[str]] = Field(None, description="URLs картинок галереи")
    
    is_featured: bool = Field(False, description="Избранный товар")
    is_bestseller: bool = Field(False, description="Бестселлер")
    
    @field_validator('discount_price')
    @classmethod
    def discount_less_than_price(cls, v, info):
        if v is not None and 'price' in info.data:
            if v >= info.data['price']:
                raise ValueError('Цена со скидкой должна быть меньше основной цены')
        return v


class ProductUpdateRequest(BaseModel):
    """Схема для обновления товара"""
    
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    category_id: Optional[int] = Field(None, gt=0)
    
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    discount_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    cost_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    
    stock_quantity: Optional[int] = Field(None, ge=0)  # ← WAS: stock (ИСПРАВЛЕНО)
    
    image_url: Optional[str] = Field(None, max_length=500)
    gallery_urls: Optional[List[str]] = Field(None)
    
    is_active: Optional[bool] = Field(None)
    is_featured: Optional[bool] = Field(None)
    is_bestseller: Optional[bool] = Field(None)


class ProductResponse(BaseModel):
    """Схема ответа товара"""
    
    id: int
    name: str
    slug: str
    category_id: int
    price: Decimal
    discount_price: Optional[Decimal]
    stock_quantity: int  # ← WAS: stock (ИСПРАВЛЕНО)
    sku: Optional[str]
    image_url: Optional[str]
    average_rating: float  # ← WAS: rating (ИСПРАВЛЕНО)
    review_count: int
    is_active: bool
    is_featured: bool
    is_bestseller: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    """Детальная схема товара"""
    
    description: Optional[str]
    cost_price: Optional[Decimal]
    gallery_urls: Optional[List[str]]
    meta_title: Optional[str]
    meta_description: Optional[str]
    tags: Optional[str]
    updated_at: datetime
    
    @property
    def available_stock(self) -> int:
        """Доступный остаток (вычисляется от stock_quantity - reserved_stock)"""
        # Примечание: reserved_stock не передаётся в схеме, вычисляется в БД
        return self.stock_quantity
    
    @property
    def discount_percent(self) -> float:
        """Процент скидки"""
        if self.discount_price and self.price:
            return ((float(self.price) - float(self.discount_price)) / float(self.price)) * 100
        return 0


class ProductListResponse(BaseModel):
    """Список товаров с пагинацией"""
    
    total: int
    skip: int
    limit: int
    products: List[ProductResponse]
