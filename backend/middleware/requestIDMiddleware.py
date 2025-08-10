from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import uuid
from starlette.responses import Response

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        reqId = request.headers.get("x-request-id", str(uuid.uuid4()))
        with logger.contextualize(request_id=reqId):
            response: Response = await call_next(request)
            response.headers["x-request-id"] = reqId
            return response