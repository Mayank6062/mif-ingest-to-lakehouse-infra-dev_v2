"""
Session service.

Frozen Reference: STEP-3 Database, STEP-5.1 Business Rules - Session lifecycle
Authority: Session persistence, restore, lifecycle management
"""

import logging
import secrets
from typing import Optional, Tuple
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User, Session
from backend.repositories import UserRepository, SessionRepository
from backend.schemas import UserDTO, SessionDTO

logger = logging.getLogger(__name__)


class SessionService:
    """Session management service."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.session_repo = SessionRepository()

    async def create_session_for_user(
        self,
        db_session: AsyncSession,
        user: User,
        timeout_seconds: int = 3600,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> SessionDTO:
        """Create new session for user."""
        try:
            # Expire any existing active sessions (one draft per session rule)
            existing_session = await self.session_repo.get_active_by_user_id(db_session, user.user_id)
            if existing_session:
                logger.info(f"Expiring previous session for user {user.user_id}")
                await self.session_repo.expire_session(db_session, existing_session.session_id)

            # Create new session
            new_session = await self.session_repo.create(
                db_session,
                user_id=user.user_id,
                timeout_seconds=timeout_seconds,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            await db_session.commit()
            
            logger.info(f"Session created: {new_session.session_id} for user {user.user_id}")
            
            return SessionDTO.from_orm(new_session)

        except Exception as e:
            await db_session.rollback()
            logger.error(f"Session creation failed: {e}")
            raise

    async def get_session(
        self,
        db_session: AsyncSession,
        session_id: UUID,
    ) -> Optional[SessionDTO]:
        """Get session by ID."""
        try:
            session = await self.session_repo.get_by_id(db_session, session_id)
            
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return None
            
            # Check expiry
            if session.is_expired:
                logger.info(f"Session expired: {session_id}")
                await self.session_repo.expire_session(db_session, session_id)
                await db_session.commit()
                return None
            
            return SessionDTO.from_orm(session)

        except Exception as e:
            logger.error(f"Get session error: {e}")
            raise

    async def restore_session(
        self,
        db_session: AsyncSession,
        session_id: UUID,
    ) -> Optional[Tuple[SessionDTO, UserDTO]]:
        """Restore session and user data (recovery flow)."""
        try:
            session = await self.session_repo.get_by_id(db_session, session_id)
            
            if not session:
                logger.warning(f"Cannot restore; session not found: {session_id}")
                return None
            
            # Check expiry
            if session.is_expired:
                logger.warning(f"Cannot restore; session expired: {session_id}")
                await self.session_repo.expire_session(db_session, session_id)
                await db_session.commit()
                return None
            
            # Update last activity
            await self.session_repo.update_last_activity(db_session, session_id)
            
            # Get user
            user = await self.user_repo.get_by_id(db_session, session.user_id)
            if not user:
                logger.error(f"User not found for session {session_id}")
                return None
            
            await db_session.commit()
            
            logger.info(f"Session restored: {session_id}")
            
            return (SessionDTO.from_orm(session), UserDTO.from_orm(user))

        except Exception as e:
            await db_session.rollback()
            logger.error(f"Session restore error: {e}")
            raise

    async def update_session_activity(
        self,
        db_session: AsyncSession,
        session_id: UUID,
    ) -> Optional[SessionDTO]:
        """Update session last activity timestamp."""
        try:
            session = await self.session_repo.update_last_activity(db_session, session_id)
            
            if session:
                await db_session.commit()
                return SessionDTO.from_orm(session)
            
            return None

        except Exception as e:
            await db_session.rollback()
            logger.error(f"Update session activity error: {e}")
            raise

    async def expire_session(
        self,
        db_session: AsyncSession,
        session_id: UUID,
    ) -> bool:
        """Expire a session."""
        try:
            session = await self.session_repo.expire_session(db_session, session_id)
            
            if session:
                await db_session.commit()
                logger.info(f"Session expired: {session_id}")
                return True
            
            return False

        except Exception as e:
            await db_session.rollback()
            logger.error(f"Expire session error: {e}")
            raise

    async def generate_state_token(self) -> str:
        """Generate CSRF state token for OAuth."""
        return secrets.token_urlsafe(32)
