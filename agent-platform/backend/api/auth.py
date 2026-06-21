"""
Authentication API routes.

Frozen Reference: STEP-2 Architecture Section 2 - OAuth callback, STEP-6 API Contracts
Authority: HTTP endpoints for Phase-1 OAuth flow
"""

import logging
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db_session
from backend.services.github_oauth import GitHubOAuthService
from backend.services.session import SessionService
from backend.repositories import UserRepository
from backend.schemas import (
    GitHubOAuthCallbackRequest,
    GitHubOAuthCallbackResponse,
    UserDTO,
    SessionDTO,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

github_oauth_service = GitHubOAuthService()
session_service = SessionService()
user_repo = UserRepository()


@router.get("/github/authorize")
async def github_authorize():
    """Initiate GitHub OAuth flow."""
    try:
        state = await session_service.generate_state_token()
        
        authorize_url = github_oauth_service.get_authorization_url(state)
        
        # In production, store state in Redis for CSRF validation
        logger.info(f"GitHub authorization initiated with state: {state}")
        
        return {
            "authorization_url": authorize_url,
            "state": state,
        }
    
    except Exception as e:
        logger.error(f"GitHub authorization error: {e}")
        raise HTTPException(status_code=500, detail="Authorization failed")


@router.get("/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...),
    db_session: AsyncSession = Depends(get_db_session),
):
    """GitHub OAuth callback handler."""
    try:
        # Validate state (in production, check against Redis)
        if not code or not state:
            raise HTTPException(status_code=400, detail="Missing code or state")
        
        # Exchange code for token
        access_token = await github_oauth_service.exchange_code_for_token(code)
        if not access_token:
            logger.error("Failed to exchange code for token")
            raise HTTPException(status_code=401, detail="Token exchange failed")
        
        # Get GitHub user info
        github_user = await github_oauth_service.get_user_info(access_token)
        if not github_user:
            logger.error("Failed to get GitHub user info")
            raise HTTPException(status_code=401, detail="User info retrieval failed")
        
        # Get GitHub user email
        github_email = await github_oauth_service.get_user_email(access_token)
        if not github_email:
            logger.error("Failed to get GitHub user email")
            raise HTTPException(status_code=401, detail="Email retrieval failed")
        
        # Check if user exists
        existing_user = await user_repo.get_by_github_id(db_session, github_user["id"])
        
        if existing_user:
            user = existing_user
            logger.info(f"Existing user found: {user.username}")
        else:
            # Create new user
            user = await user_repo.create(
                db_session,
                username=github_user["login"],
                email=github_email,
                github_id=github_user["id"],
                github_login=github_user["login"],
                github_avatar_url=github_user.get("avatar_url"),
            )
            logger.info(f"New user created: {user.username}")
        
        # Create session
        session_dto = await session_service.create_session_for_user(
            db_session,
            user,
            ip_address=None,  # TODO: Extract from request
            user_agent=None,  # TODO: Extract from request
        )
        
        # Prepare response
        response = GitHubOAuthCallbackResponse(
            session_id=session_dto.session_id,
            user=UserDTO.from_orm(user),
            redirect_url="http://localhost:3000/dashboard",
        )
        
        logger.info(f"OAuth callback successful for user: {user.username}")
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GitHub callback error: {e}")
        raise HTTPException(status_code=500, detail="Callback processing failed")


@router.get("/session/{session_id}", response_model=SessionDTO)
async def get_session(
    session_id: str,
    db_session: AsyncSession = Depends(get_db_session),
):
    """Get current session (Phase-1)."""
    try:
        from uuid import UUID
        session_uuid = UUID(session_id)
        
        session_dto = await session_service.get_session(db_session, session_uuid)
        
        if not session_dto:
            raise HTTPException(status_code=404, detail="Session not found or expired")
        
        return session_dto
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    except Exception as e:
        logger.error(f"Get session error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session")


@router.post("/logout")
async def logout(
    session_id: str = Query(...),
    db_session: AsyncSession = Depends(get_db_session),
):
    """Logout (expire session)."""
    try:
        from uuid import UUID
        session_uuid = UUID(session_id)
        
        success = await session_service.expire_session(db_session, session_uuid)
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"status": "logged_out"}
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")
