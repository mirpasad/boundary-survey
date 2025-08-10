import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings
from fastapi.responses import JSONResponse
from loguru import logger

class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=settings.GLOBAL_REQUEST_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.error(f"Request timed out for {request.url.path}")
            return JSONResponse(
                status_code=504,  # Gateway Timeout
                content={"error": {
                    "message": "Request timed out", 
                    "code": "TIMEOUT_ERROR"
                    }
                }
            )