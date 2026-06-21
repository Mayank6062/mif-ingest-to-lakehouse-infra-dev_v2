"""
Health check endpoint.

Frozen Reference: STEP-2 Architecture Section 2, STEP-11.2 Monitoring
Authority: Foundation API for health checks
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db_session, db_manager
from backend.core.config import get_settings
from backend.schemas import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db_session: AsyncSession = Depends(get_db_session),
):
    """Health check endpoint."""
    settings = get_settings()
    
    health_status = "health"
    db_status = "connected"
    redis_status = "connected"
    
    try:
        # Check database
        await db_session.execute("SELECT 1")
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        db_status = "disconnected"
        health_status = "degraded"
    
    try:
        # Check Redis (basic connectivity)
        # TODO: Implement Redis health check
        pass
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        redis_status = "disconnected"
        health_status = "degraded"
    
    return HealthResponse(
        status=health_status,
        timestamp=datetime.utcnow(),
        database=db_status,
        redis=redis_status,
        version="0.1.0",
    )
