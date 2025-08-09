import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        with logger.contextualize(request_id=rid):
            response: Response = await call_next(request)
            response.headers["x-request-id"] = rid
            return response
