"""
Repository layer for data access.

Frozen Reference: STEP-10 Database Persistence Freeze
Authority: Data access abstraction layer
"""

from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.models import User, Session, RoleType


__all__ = ["UserRepository", "SessionRepository"]


class UserRepository:
    """User data access."""

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_github_id(session: AsyncSession, github_id: int) -> Optional[User]:
        """Get user by GitHub ID."""
        result = await session.execute(select(User).where(User.github_id == github_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> Optional[User]:
        """Get user by username."""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        session: AsyncSession,
        username: str,
        email: str,
        github_id: int,
        github_login: str,
        github_avatar_url: Optional[str] = None,
    ) -> User:
        """Create new user."""
        user = User(
            username=username,
            email=email,
            github_id=github_id,
            github_login=github_login,
            github_avatar_url=github_avatar_url,
            role=RoleType.CONTRIBUTOR,  # Default role
        )
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def update(session: AsyncSession, user: User) -> User:
        """Update user."""
        await session.merge(user)
        await session.flush()
        return user


class SessionRepository:
    """Session data access."""

    @staticmethod
    async def get_by_id(session: AsyncSession, session_id: UUID) -> Optional[Session]:
        """Get session by ID."""
        result = await session.execute(select(Session).where(Session.session_id == session_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_active_by_user_id(session: AsyncSession, user_id: UUID) -> Optional[Session]:
        """Get active session for user (only one active session per user)."""
        result = await session.execute(
            select(Session).where(
                (Session.user_id == user_id) &
                (Session.status == "ACTIVE") &
                (Session.expires_at > datetime.utcnow())
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        session: AsyncSession,
        user_id: UUID,
        timeout_seconds: int = 3600,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Session:
        """Create new session."""
        expires_at = datetime.utcnow() + timedelta(seconds=timeout_seconds)
        
        new_session = Session(
            user_id=user_id,
            status="ACTIVE",
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
        )
        session.add(new_session)
        await session.flush()
        return new_session

    @staticmethod
    async def update_last_activity(session: AsyncSession, session_id: UUID):
        """Update session last activity."""
        result = await session.execute(select(Session).where(Session.session_id == session_id))
        sess = result.scalar_one_or_none()
        if sess:
            sess.update_last_activity()
            await session.flush()
            return sess
        return None

    @staticmethod
    async def expire_session(session: AsyncSession, session_id: UUID):
        """Expire session."""
        result = await session.execute(select(Session).where(Session.session_id == session_id))
        sess = result.scalar_one_or_none()
        if sess:
            sess.status = "EXPIRED"
            await session.flush()
            return sess
        return None

    @staticmethod
    async def cleanup_expired(session: AsyncSession):
        """Cleanup expired sessions (CRON job)."""
        # Update status for expired sessions
        await session.execute(
            select(Session).where(Session.expires_at < datetime.utcnow())
        )
        # In production, delete old expired sessions after retention period
