# backend/app/schemas/category.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CategoryCreateRequest(BaseModel):
    """Схема для создания категории"""
    
    name: str = Field(..., min_length=2, max_length=200, description="Название категории")
    slug: str = Field(..., min_length=2, max_length=200, description="URL slug")
    description: Optional[str] = Field(None, max_length=1000, description="Описание")
    image_url: Optional[str] = Field(None, max_length=500, description="URL картинки")
    display_order: int = Field(0, ge=0, description="Порядок отображения")


class CategoryUpdateRequest(BaseModel):
    """Схема для обновления категории"""
    
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = Field(None)
    display_order: Optional[int] = Field(None, ge=0)


class CategoryResponse(BaseModel):
    """Схема ответа категории"""
    
    id: int
    name: str
    slug: str
    description: Optional[str]
    image_url: Optional[str]
    is_active: bool
    display_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryDetailResponse(CategoryResponse):
    """Детальная схема категории"""
    
    updated_at: datetime
