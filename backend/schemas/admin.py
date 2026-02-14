# backend/app/schemas/admin.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class AdminProductBulkUploadRequest(BaseModel):
    """Схема для массовой загрузки товаров"""
    
    file_url: str = Field(..., description="URL CSV файла")


class AdminAuditLogResponse(BaseModel):
    """Схема логов аудита"""
    
    id: int
    user_id: Optional[int]
    action: str
    entity_type: str
    entity_id: int
    old_values: Optional[dict]
    new_values: Optional[dict]
    ip_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdminDashboardMetrics(BaseModel):
    """Метрики дашборда"""
    
    total_orders: int = Field(..., description="Всего заказов")
    total_revenue: Decimal = Field(..., description="Общий доход")
    today_revenue: Decimal = Field(..., description="Доход за сегодня")
    new_users: int = Field(..., description="Новых пользователей")
    active_products: int = Field(..., description="Активных товаров")
    pending_orders: int = Field(..., description="Ожидающих заказов")


class AdminOrderStatsResponse(BaseModel):
    """Статистика по заказам"""
    
    total_orders: int
    pending: int
    processing: int
    shipped: int
    delivered: int
    cancelled: int
    refunded: int


class AdminUserManagementRequest(BaseModel):
    """Схема для управления пользователем"""
    
    action: str = Field(..., regex=r"^(block|unblock|make_admin|revoke_admin)$")
    reason: Optional[str] = Field(None, max_length=500)


class AdminPermissionsResponse(BaseModel):
    """Схема прав доступа"""
    
    role: str
    permissions: dict
    
    class Config:
        from_attributes = True
