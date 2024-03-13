"""Moonhub API
Start the proxy server using uvicorn to run FastAPI
"""
import os
from time import sleep
from loguru import logger
from uvicorn import Server, Config
from src.common.logging import init_logging, sink_serializer

# load our config
# from src.common.config import Settings # pylint: disable=C0413,E0401
from src.common.config import settings

# remove default logging and setup our custom sink serializer
logger.remove()
logger.add(sink_serializer, level=settings.log_level)

# kick off the server
if __name__ == "__main__":
    server = Server(
        Config(
            "src.entry:app",
            host=settings.listen_address,
            port=settings.port,
            reload=settings.reload,
        )
    )

    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    init_logging()

    # run the server
    server.run()
