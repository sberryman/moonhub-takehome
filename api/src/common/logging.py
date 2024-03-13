import json
import logging
import sys
from datetime import datetime

from loguru import logger


def sink_serializer(message):
    """Very simplified serializer for json logging"""
    record = message.record
    simplified = {
        "level": record["level"].name,
        "msg": record["message"],
        "time": datetime.strftime(record["time"], "%Y-%m-%dT%H:%M:%SZ"),
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
    }

    if "extra" in record:
        extra = record["extra"]
        if "extra" in extra:
            extra = extra["extra"]

        if "request_json_fields" in extra:
            for key, value in extra["request_json_fields"].items():
                simplified[key] = value

            # remove line
            del simplified["line"]

            if not isinstance(record["message"], str) or len(record["message"]) == 0:
                del simplified["msg"]

    serialized = json.dumps(simplified)
    print(serialized, file=sys.stdout)


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init_logging():
    """
    Replaces logging handlers with a handler for using the custom handler.

    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format
    >>> app.add_event_handler("startup", init_logging)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.
    """

    # disable handlers for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    # works with uvicorn==0.11.6
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
        or name.startswith("torch.")
        or name.startswith("asyncio.")
    )
    for _logger in loggers:
        _logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("torch").handlers = [intercept_handler]
    logging.getLogger("asyncio").handlers = [intercept_handler]
