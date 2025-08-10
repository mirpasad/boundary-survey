import asyncio
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_504_GATEWAY_TIMEOUT
from core.config import settings

# Middleware that enforces a global timeout for all incoming requests.
# If a request exceeds the configured timeout, a 504 Gateway Timeout error is returned.
class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=settings.GLOBAL_REQUEST_TIMEOUT
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=HTTP_504_GATEWAY_TIMEOUT,
                detail="Request processing time exceeded"
            )