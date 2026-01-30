from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(description="Mail")
    username: str = Field(description="Username")
    is_active: bool = Field(description="Active", default=True)
    is_verified: bool = Field(description="Verified", default=False)


class UserCreate(UserBase):
    password: str = Field(description="Password")

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if v.islower():
            raise ValueError("Password must contain one uppercase sym")
        if not set('!@#$%&*').intersection(v):
            raise ValueError(
                "Password must contain at least one symbol like(! @ # $ % & *)"
            )
        return v


class UserResponse(UserBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
