"""
Database ORM models.

Frozen Reference: STEP-10 Database Persistence Freeze - Tables: users, sessions
Authority: SQLAlchemy declarative models
"""

from datetime import datetime, timedelta
from typing import Optional
import uuid

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Index, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from backend.database import Base


class RoleType(str, enum.Enum):
    """RBAC role types (frozen in STEP-11.3)."""
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"
    REVIEWER = "reviewer"
    READ_ONLY = "read_only"


class User(Base):
    """User model (ORM)."""

    __tablename__ = "users"

    # Primary key
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Unique fields
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # GitHub OAuth
    github_id = Column(Integer, unique=True, nullable=False, index=True)
    github_login = Column(String(255), nullable=False)
    github_avatar_url = Column(String(512), nullable=True)

    # Role (Phase-2: RBAC model)
    role = Column(Enum(RoleType), nullable=False, default=RoleType.CONTRIBUTOR)

    # Metadata
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_users_github_id", "github_id"),
        Index("ix_users_is_active", "is_active"),
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, github_login={self.github_login})>"


class Session(Base):
    """Session model (ORM)."""

    __tablename__ = "sessions"

    # Primary key
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)

    # Session state (frozen in STEP-9 State Model)
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE, EXPIRED, CLOSED
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(512), nullable=True)

    # Pointers to active draft (frozen in STEP-9 State Model)
    active_draft_id = Column(UUID(as_uuid=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    last_activity = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")

    # Indexes
    __table_args__ = (
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_status", "status"),
        Index("ix_sessions_expires_at", "expires_at"),
    )

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id}, status={self.status})>"

    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_active(self) -> bool:
        """Check if session is active."""
        return self.status == "ACTIVE" and not self.is_expired

    def update_last_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
