"""
GitHub OAuth service.

Frozen Reference: STEP-2 Architecture Section 2 - OAuth Architecture
Authority: Server-side OAuth token exchange (NO token storage in LangGraph state)
"""

import httpx
import logging
from typing import Optional

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


class GitHubOAuthService:
    """GitHub OAuth server-side exchange (frozen)."""

    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_API_URL = "https://api.github.com"

    def __init__(self):
        self.settings = get_settings()

    def get_authorization_url(self, state: str) -> str:
        """Generate GitHub OAuth authorization URL."""
        params = {
            "client_id": self.settings.GITHUB_CLIENT_ID,
            "redirect_uri": self.settings.GITHUB_CALLBACK_URL,
            "scope": "user:email",
            "state": state,
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.GITHUB_AUTH_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str) -> Optional[str]:
        """Exchange authorization code for access token (server-side)."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.GITHUB_TOKEN_URL,
                    data={
                        "client_id": self.settings.GITHUB_CLIENT_ID,
                        "client_secret": self.settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                
                if response.status_code != 200:
                    logger.error(f"GitHub token exchange failed: {response.status_code}")
                    return None
                
                data = response.json()
                token = data.get("access_token")
                
                if not token:
                    logger.error("No access token in GitHub response")
                    return None
                
                logger.info("GitHub OAuth token exchanged successfully")
                return token
                
        except Exception as e:
            logger.error(f"GitHub token exchange error: {e}")
            return None

    async def get_user_info(self, access_token: str) -> Optional[dict]:
        """Get GitHub user info using access token."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.GITHUB_API_URL}/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                
                if response.status_code != 200:
                    logger.error(f"GitHub user info fetch failed: {response.status_code}")
                    return None
                
                user_data = response.json()
                logger.info(f"GitHub user info fetched: {user_data.get('login')}")
                return user_data
                
        except Exception as e:
            logger.error(f"GitHub user info error: {e}")
            return None

    async def get_user_email(self, access_token: str) -> Optional[str]:
        """Get primary GitHub user email."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.GITHUB_API_URL}/user/emails",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                
                if response.status_code != 200:
                    logger.error(f"GitHub email fetch failed: {response.status_code}")
                    return None
                
                emails = response.json()
                
                # Find primary email
                for email in emails:
                    if email.get("primary"):
                        return email.get("email")
                
                # Fallback to first email
                if emails:
                    return emails[0].get("email")
                
                return None
                
        except Exception as e:
            logger.error(f"GitHub email fetch error: {e}")
            return None
