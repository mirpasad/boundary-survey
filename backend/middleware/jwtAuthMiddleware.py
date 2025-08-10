import re
import uuid
from utils import publicPaths
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
from core.jwt import decode_jwt
from utils.publicPaths import publicPaths
from jwt import InvalidTokenError

# Middleware for validating JWT tokens on incoming requests.
# Skips validation for allow-listed public paths and CORS preflight requests.
# Attaches user claims to request state for downstream usage.
class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Validates JWT on every request, except allow-listed paths and OPTIONS."""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        COMPILED_PATTERNS = [re.compile(pattern) for pattern in publicPaths]

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
        # Returns a 401 response with a request ID for unauthorized access.
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        resp = JSONResponse(status_code=401, content={"detail": message})
        resp.headers["x-request-id"] = rid
        return resp