"""
User Service

Business logic for user management operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.auth import UserCreate


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Get user by ID
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get user by email address
    
    Args:
        db: Database session
        email: User email address
        
    Returns:
        User object or None if not found
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Create a new user
    
    Args:
        db: Database session
        user_data: User creation data
        
    Returns:
        Created User object
    """
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user object
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        phone=user_data.phone,
        organization=user_data.organization,
        bio=user_data.bio
    )
    
    # Add to database
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def update_user(db: AsyncSession, user_id: int, user_data: dict) -> Optional[User]:
    """
    Update user information
    
    Args:
        db: Database session
        user_id: User ID to update
        user_data: Updated user data
        
    Returns:
        Updated User object or None if not found
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    # Update fields
    for field, value in user_data.items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


async def activate_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Activate a user account
    
    Args:
        db: Database session
        user_id: User ID to activate
        
    Returns:
        Updated User object or None if not found
    """
    return await update_user(db, user_id, {"is_active": True})


async def deactivate_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Deactivate a user account
    
    Args:
        db: Database session
        user_id: User ID to deactivate
        
    Returns:
        Updated User object or None if not found
    """
    return await update_user(db, user_id, {"is_active": False})
