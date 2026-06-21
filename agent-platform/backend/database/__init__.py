"""
Database configuration and session management.

Frozen Reference: STEP-10 Database Persistence Freeze
Authority: SQLAlchemy 2.0+ ORM with async support
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
import logging

from backend.core.config import get_settings

logger = logging.getLogger(__name__)

# ORM declarative base for all models
Base = declarative_base()


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self):
        self.settings = get_settings()
        self.engine = None
        self.async_session_maker = None

    async def initialize(self):
        """Initialize async database engine."""
        try:
            # Convert postgresql:// to postgresql+asyncpg://
            db_url = self.settings.DATABASE_URL.replace(
                "postgresql://", "postgresql+asyncpg://"
            )

            # Connection pool configuration
            poolclass = NullPool if self.settings.ENVIRONMENT == "testing" else QueuePool

            self.engine = create_async_engine(
                db_url,
                echo=self.settings.DATABASE_ECHO,
                pool_size=self.settings.DATABASE_POOL_SIZE,
                max_overflow=10,
                pool_timeout=self.settings.DATABASE_POOL_TIMEOUT,
                pool_recycle=self.settings.DATABASE_POOL_RECYCLE,
                pool_pre_ping=True,
                poolclass=poolclass if self.settings.ENVIRONMENT != "testing" else None,
            )

            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            logger.info(f"Database initialized: {self.settings.ENVIRONMENT}")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    async def close(self):
        """Close all connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")

    async def create_all_tables(self):
        """Create all tables (for development/testing)."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("All tables created")

    async def drop_all_tables(self):
        """Drop all tables (for testing)."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("All tables dropped")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session (dependency injection)."""
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Session error: {e}")
                raise
            finally:
                await session.close()


# Singleton instance
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session."""
    async for session in db_manager.get_session():
        yield session
