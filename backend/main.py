from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from core.config import settings
from core.logging import setup_logging
from core.rate_limit import limiter
from router import routers
from utils.middleware import RequestIDMiddleware, JWTAuthMiddleware
from core.redis import redis_client

logger = setup_logging()

app = FastAPI(title="Survey Generator API", docs_url="/docs", version="1.0.0")
app.state.limiter = limiter

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    JWTAuthMiddleware,
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SlowAPIMiddleware)

# Include all routers from the router package
for router in routers:
    app.include_router(router, prefix=settings.API_PREFIX, tags=[router.tags])


@app.on_event("startup")
async def startup_event():
    await redis_client.connect()
    logger.info("Redis connected")

@app.on_event("shutdown")
async def shutdown_event():
    if redis_client.client:
        await redis_client.client.close()
        logger.info("Redis disconnected")
        
@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})