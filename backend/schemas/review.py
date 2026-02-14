# backend/app/schemas/review.py

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ReviewCreateRequest(BaseModel):
    """Схема для создания отзыва"""
    
    product_id: int = Field(..., gt=0, description="ID товара")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг от 1 до 5")
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Заголовок отзыва")
    comment: Optional[str] = Field(None, min_length=10, max_length=5000, description="Текст отзыва")
    
    @validator('comment')
    def comment_min_length(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError('Комментарий должен быть минимум 10 символов')
        return v


class ReviewUpdateRequest(BaseModel):
    """Схема для обновления отзыва"""
    
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    comment: Optional[str] = Field(None, min_length=10, max_length=5000)


class ReviewResponse(BaseModel):
    """Схема ответа отзыва"""
    
    id: int
    product_id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str]
    rating: int
    title: Optional[str]
    comment: Optional[str]
    helpful_count: int
    unhelpful_count: int
    is_verified_purchase: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    """Список отзывов"""
    
    total: int
    average_rating: float
    reviews: list[ReviewResponse]


class ReviewStatisticsResponse(BaseModel):
    """Статистика отзывов"""
    
    total_reviews: int
    average_rating: float
    rating_distribution: dict[int, int]  # {5: 100, 4: 50, ...}
