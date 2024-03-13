"""
Routes: API V1
"""
from fastapi import APIRouter

from src.routes.v1.sample.main import router as sample_router

# no auth for healthcheck
router = APIRouter(
    prefix="/v1",
)

# include all of our v1 routes!
router.include_router(sample_router)
