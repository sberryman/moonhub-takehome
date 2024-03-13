"""
Routes: API
"""
from fastapi import APIRouter

from src.routes.v1 import v1

# no auth for healthcheck
router = APIRouter()

# include our v1 routes
# this is here incase we eventually include a v2, v3, etc.
router.include_router(v1.router)
