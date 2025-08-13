from middleware.timeoutMiddleware import TimeoutMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from core.config import settings
from core.logging import setup_logging
from core.rate_limit import limiter
from router import routers
from middleware.jwtAuthMiddleware import JWTAuthMiddleware
from middleware.requestIDMiddleware import RequestIDMiddleware
from core.redis import redis_client

logger = setup_logging()

# Entry point for the backend FastAPI application.
# Sets up middleware, CORS, rate limiting, authentication, and router inclusion.
app = FastAPI(title="Survey Generator API", docs_url="/docs", version="1.0.0")
app.state.limiter = limiter

# Configure allowed CORS origins for frontend integration.
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTAuthMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimeoutMiddleware)
app.add_middleware(SlowAPIMiddleware)

# Include all routers from the router package for modular API endpoints.
for router in routers:
    app.include_router(router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    # Initialize Redis connection on app startup.
    await redis_client.connect()
    logger.info("Redis connected")

@app.on_event("shutdown")
async def shutdown_event():
    # Gracefully close Redis connection on app shutdown.
    if redis_client.client:
        await redis_client.client.close()
        logger.info("Redis disconnected")
        
@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request, exc):
    # Custom handler for rate limit exceeded errors.
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})