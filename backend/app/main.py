from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.rate_limit import limiter
from app.api.routes import router
from app.utils.middleware import RequestIDMiddleware

logger = setup_logging()

app = FastAPI(title="Survey Generator API", version="1.0.0")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIDMiddleware)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/health")
def health():
    return {"ok": True}

@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
