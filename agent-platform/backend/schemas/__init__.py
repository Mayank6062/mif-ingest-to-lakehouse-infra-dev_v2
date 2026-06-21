"""
Pydantic DTOs for API contracts.

Frozen Reference: STEP-6.1 DTO Freeze, STEP-9.1 DTO v1.0.0 schemas
Authority: All DTOs frozen; v1.0.0 schema locked
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# === UserDTO ===

class UserDTO(BaseModel):
    """User data transfer object (v1.0.0 frozen)."""

    user_id: UUID
    username: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    github_login: str
    github_avatar_url: Optional[str] = None
    role: str = Field(..., description="User role: admin, contributor, reviewer, read_only")
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# === SessionDTO ===

class SessionDTO(BaseModel):
    """Session data transfer object (v1.0.0 frozen)."""

    session_id: UUID
    user_id: UUID
    status: str = Field(..., description="Session status: ACTIVE, EXPIRED, CLOSED")
    active_draft_id: Optional[UUID] = None
    ip_address: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


# === Auth DTOs ===

class GitHubOAuthCallbackRequest(BaseModel):
    """GitHub OAuth callback request (frozen)."""

    code: str = Field(..., description="Authorization code from GitHub")
    state: str = Field(..., description="State parameter for CSRF protection")


class GitHubOAuthCallbackResponse(BaseModel):
    """GitHub OAuth callback response (frozen)."""

    session_id: UUID
    user: UserDTO
    redirect_url: str = "http://localhost:3000/dashboard"


class HealthResponse(BaseModel):
    """Health check response (frozen)."""

    status: str = Field(..., description="health, degraded, unhealthy")
    timestamp: datetime
    database: str = "connected"
    redis: str = "connected"
    version: str = "0.1.0"
