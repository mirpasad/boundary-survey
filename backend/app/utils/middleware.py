import re
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger
from starlette.responses import JSONResponse
from starlette.requests import Request
from typing import Iterable, Optional, Set
from app.core.jwt import decode_jwt
from .publicPaths import publicPaths
from jwt import InvalidTokenError

COMPILED_PATTERNS = [re.compile(pattern) for pattern in publicPaths]
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        reqId = request.headers.get("x-request-id", str(uuid.uuid4()))
        with logger.contextualize(request_id=reqId):
            response: Response = await call_next(request)
            response.headers["x-request-id"] = reqId
            return response

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Validates JWT on every request, except allow-listed paths and OPTIONS."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        isAllowedPath = any(pattern.match(path) for pattern in COMPILED_PATTERNS)
        # Allow CORS preflight and selected public endpoints
        if request.method == "OPTIONS" or isAllowedPath:
            return await call_next(request)

        auth = request.headers.get("authorization") or request.headers.get("Authorization")
        if not auth or not auth.lower().startswith("bearer "):
            return self._unauthorized(request, "Missing or invalid Authorization header")

        token = auth.split(" ", 1)[1].strip()
        try:
            payload = decode_jwt(token)
            request.state.user = payload  # attach claims for downstream usage
        except InvalidTokenError as e:
            return self._unauthorized(request, f"Invalid token: {str(e)}")
        except Exception:
            return self._unauthorized(request, "Could not validate credentials")

        return await call_next(request)

    def _unauthorized(self, request: Request, message: str) -> JSONResponse:
        # Ensure every response has an x-request-id even if we short-circuit here.
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        resp = JSONResponse(status_code=401, content={"detail": message})
        resp.headers["x-request-id"] = rid
        return resp