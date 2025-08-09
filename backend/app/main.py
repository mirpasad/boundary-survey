from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import orjson

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import router
from app.core.rate_limit import limiter

logger = setup_logging()

def ORJSONResponse(obj):
    return orjson.dumps(obj)

app = FastAPI(title="Survey Generator API", version="1.0.0")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount routes
app.include_router(router, prefix=settings.API_PREFIX)

# rate limit error
@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# root
@app.get("/health")
def health():
    return {"ok": True}
