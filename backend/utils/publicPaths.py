# List of regex patterns for public API endpoints.
# Requests matching these paths bypass authentication middleware.

publicPaths = [
    r"^/api/health$",          # health
    r"^/api/public/.*$",       # any /api/public/*
    r"^/api/?$",               # /api or /api/
    r"^/docs$",                # FastAPI docs
    r"^/openapi\.json$",       # OpenAPI schema
    r"^/api/auth/.*$",         # auth endpoints
]