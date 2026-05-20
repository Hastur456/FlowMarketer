from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime
from fastapi_users import schemas
from uuid import UUID


class UserRead(schemas.BaseUser[UUID]):
    first_name: str|None = Field(default=None, max_length=100)
    last_name: str|None = Field(default=None, max_length=100)
    phone: PhoneNumber|None = Field(default=None)


class UserCreate(schemas.BaseUserCreate):
    first_name: str|None = Field(default=None, max_length=100)
    last_name: str|None = Field(default=None, max_length=100)
    phone: PhoneNumber|None = Field(default=None, examples=["+79000000000", "+447700900123"])


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str|None = Field(default=None, max_length=100)
    last_name: str|None = Field(default=None, max_length=100)
    phone: PhoneNumber|None = Field(default=None, examples=["+79000000000", "+447700900123"])


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Email адрес пользователя")
    password: str = Field(..., min_length=8, description="Пароль минимум 8 символов")
    first_name: str = Field(..., min_length=2, max_length=100, description="Имя")
    last_name: str = Field(..., min_length=2, max_length=100, description="Фамилия")
    phone: str | None = Field(None, pattern=r"^\+?[0-9\-\s\(\)]{10,}$", description="Номер телефона")
    
    @field_validator('password')
    def password_valid(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать заглавные буквы')
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать цифры')
        if not any(char in '!@#$%^&*' for char in v):
            raise ValueError('Пароль должен содержать спецсимволы (!@#$%^&*)')
        return v


class UserLoginRequest(BaseModel):
    """Схема для входа"""
    
    email: EmailStr = Field(..., description="Email адрес")
    password: str = Field(..., description="Пароль")
    remember_me: bool = Field(False, description="Запомнить меня")


class UserUpdateRequest(BaseModel):
    """Схема для обновления профиля"""
    
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\-\s\(\)]{10,}$")
    avatar_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = Field(None, max_length=500)
    preferred_language: str = Field('ru', pattern=r"^(ru|en)$")


class UserPasswordChangeRequest(BaseModel):
    """Схема для смены пароля"""
    
    old_password: str = Field(..., description="Старый пароль")
    new_password: str = Field(..., min_length=8, description="Новый пароль")
    confirm_password: str = Field(..., description="Подтверждение пароля")
    
    @field_validator('new_password')
    def password_valid(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать заглавные буквы')
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать цифры')
        return v
    
    @field_validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Пароли не совпадают')
        return v


class UserForgotPasswordRequest(BaseModel):
    """Схема для восстановления пароля"""
    
    email: EmailStr = Field(..., description="Email адрес")


class UserResetPasswordRequest(BaseModel):
    """Схема для установки нового пароля"""
    
    token: str = Field(..., description="Токен восстановления")
    new_password: str = Field(..., min_length=8, description="Новый пароль")
    confirm_password: str = Field(..., description="Подтверждение пароля")


class UserResponse(BaseModel):
    """Схема ответа пользователя"""
    
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    is_admin: bool
    is_active: bool
    is_blocked: bool
    email_verified_at: Optional[datetime]
    two_factor_enabled: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Детальная схема пользователя"""
    
    preferred_language: str
    updated_at: datetime


class TokenResponse(BaseModel):
    """Схема ответа с токенами"""
    
    access_token: str = Field(..., description="Access токен (24 часа)")
    refresh_token: str = Field(..., description="Refresh токен (7 дней)")
    token_type: str = Field("bearer", description="Тип токена")
    expires_in: int = Field(86400, description="Время жизни в секундах")
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Схема для обновления токена"""
    
    refresh_token: str = Field(..., description="Refresh токен")


class TwoFactorEnableRequest(BaseModel):
    """Схема для включения 2FA"""
    
    password: str = Field(..., description="Пароль подтверждения")


class TwoFactorVerifyRequest(BaseModel):
    """Схема для проверки 2FA кода"""
    
    code: str = Field(..., pattern=r"^\d{6}$", description="6-значный код")


class ResendVerificationEmailRequest(BaseModel):
    """Схема для повторной отправки верификации"""
    
    email: EmailStr = Field(..., description="Email адрес")


