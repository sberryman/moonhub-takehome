"""
Routes: Healthcheck
"""
from fastapi import APIRouter
from pydantic import BaseModel

from .broker import router as redis_router
from .db import prisma

# no auth for healthcheck
router = APIRouter(tags=["healthcheck"])


class HealthCheckResponse(BaseModel):
    """Health check response model"""

    healthy: bool


@router.get("/healthcheck", response_model=HealthCheckResponse)
async def healthcheck():
    """Simple healthcheck endpoint, extend with downstream healthchecks"""
    # downstream checks
    try:
        # ensure we can query the db
        await prisma.query_raw("SELECT 1")

        # how about redis?
        # await redis_router.ping()
        await redis_router.broker._connection.ping()

        return {"healthy": True}
    except Exception:
        return {"healthy": False}
