from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    id: str = Field(...)
    email: EmailStr = Field(description="Mail")
    username: str = Field(description="Username")
    is_active: bool = Field(description="Active")
    is_verified: bool = Field(description="Verified")


class UserCreate(UserBase):
    pass


class UserResponce(UserBase):
    created_at: str = Field(...)
    updated_at: str = Field(...)


class UserUpdate(BaseModel):
    id: Optional[str] = Field(...)
    email: Optional[EmailStr] = Field(default=None, description="Mail")
    username: Optional[str] = Field(default=None, description="Username")
    hashed_password: Optional[str] = Field(
        default=None,
        description="Новый пароль"
    )
    is_active: Optional[bool] = Field(default=None, description="Active")
    is_verified: Optional[bool] = Field(default=None, description="Verified")
    created_at: Optional[str] = Field(default=None)
    updated_at: str = Field(description="UPD time")
