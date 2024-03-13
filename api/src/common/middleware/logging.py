import dataclasses
import http
import logging
import math
import time
from typing import ClassVar

from fastapi import Request, Response
from loguru import logger
from pydantic import BaseModel
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import Receive

EMPTY_VALUE = ""
PORT = "8000"
PASS_ROUTES = [
    "/openapi.json",
    "/docs",
    "/healthcheck",
]


class RequestJsonLogSchema(BaseModel):
    """
    Schema for request/response answer
    """

    method: str
    path: str
    status: int
    latency: int

    module: str
    function: str


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call.
    https://github.com/tiangolo/fastapi/issues/394#issuecomment-994665859
    """

    receive: Receive
    cached_body: bytes
    _is_first_call: ClassVar[bool] = True

    async def __call__(self):
        # First call will be for getting request body => returns cached result
        if self._is_first_call:
            self._is_first_call = False
            return {
                "type": "http.request",
                "body": self.cached_body,
                "more_body": False,
            }

        return await self.receive()


class LoggingMiddleware:
    """Middleware that saves logs to JSON
    The main problem is
    After getting request_body
        body = await request.body()
    Body is removed from requests. I found solution as ReceiveProxy
    """

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint, *args, **kwargs
    ):
        # logger.debug(f"Started Middleware: {__name__}")
        start_time = time.time()
        exception_object = None
        request_headers: dict = dict(request.headers.items())

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            logging.error(f"Exception: {ex}")
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
        else:
            dict(response.headers.items())
            response_body = b""

            async for chunk in response.body_iterator:
                response_body += chunk

            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        # pass /openapi.json /docs
        if request.url.path in PASS_ROUTES:
            return response

        duration: int = math.ceil((time.time() - start_time) * 1000)

        # Initializing of json fields
        request_json_fields = RequestJsonLogSchema(
            # Request side
            method=request.method,
            path=request.url.path,
            request_headers=request_headers,
            module=request.scope["endpoint"].__module__,
            function=request.scope["endpoint"].__name__,
            # Response side
            status=response.status_code,
            latency=duration,
        ).model_dump()

        logger.info(
            "",
            extra={
                "request_json_fields": request_json_fields,
            },
            exc_info=exception_object,
        )
        return response
