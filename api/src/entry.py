"""
Main API Entrypoint
"""
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.common.broker import router as redis_router
from src.common.config import settings
from src.common.db import prisma
from src.common.healthcheck import router as healthcheck_router
from src.common.lifespans import Lifespans
from src.common.middleware.logging import LoggingMiddleware
from src.routes import routes as api


# lifespan replaces the old on_event("startup") and on_event("shutdown")
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup Event... Only really used for debugging"""
    if settings.debug is True:
        # save the openapi schema
        logger.debug("Saving openapi schema...")
        with open("openapi.json", "w", encoding="utf-8") as f_out:
            json.dump(app.openapi(), f_out, indent=4)

    # connect to the database
    logger.debug("Connecting to the database...")
    await prisma.connect()

    # do your app things
    yield

    # shutdown event

    # disconnect from the database
    logger.debug("Disconnecting from the database...")
    await prisma.disconnect()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    lifespan=Lifespans(
        [
            redis_router.lifespan_context,
            lifespan,
        ]
    )
    # lifespan=kafka_router.lifespan_context
)

if settings.debug:
    # CORS
    logger.debug("Debug CORS configuration is enabled")
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.middleware("http")(LoggingMiddleware())

# include our routes
app.include_router(redis_router)
app.include_router(api.router)
app.include_router(healthcheck_router)
