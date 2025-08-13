"""
Authentication Schemas

Pydantic models for authentication-related requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    organization: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str
    role: UserRole = UserRole.PARTICIPANT


class UserUpdate(BaseModel):
    """Schema for user profile updates"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user data in responses"""
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication tokens"""
    access_token: str
    token_type: str
    expires_in: int  # Seconds until expiration


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
