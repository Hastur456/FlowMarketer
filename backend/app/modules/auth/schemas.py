from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
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
