"""
User Model

This module defines the User model for authentication and user management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    ORGANIZER = "organizer"
    VOLUNTEER = "volunteer"
    PARTICIPANT = "participant"


class User(Base):
    """User model for authentication and basic user information"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.PARTICIPANT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Profile information
    phone = Column(String(20), nullable=True)
    organization = Column(String(255), nullable=True)
    bio = Column(String(1000), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
