"""
Database Configuration and Connection Management

This module handles database setup, connection management, and session creation.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create async engine
if settings.DATABASE_URL.startswith("sqlite"):
    # For SQLite, we need to use aiosqlite
    database_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    engine = create_async_engine(
        database_url, 
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    # For PostgreSQL, use asyncpg
    database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(database_url, echo=settings.DEBUG)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


async def get_db() -> AsyncSession:
    """
    Dependency to get database session
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    try:
        # Import all models here to ensure they are registered
        from app.models import (
            user, volunteer, participant, budget, vendor, 
            workflow, booth, feedback, certificate, media, admin
        )
        
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def close_db():
    """Close database connections"""
    await engine.dispose()
