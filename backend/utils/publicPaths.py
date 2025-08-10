# List of regex patterns for public API endpoints.
# Requests matching these paths bypass authentication middleware.

publicPaths = [
    r"^/api/health$",         # Exact match for /health
    r"^/api/public/.*$",      # Allow all paths starting with /public/
    r"^/api/$",               # Allow root path
    r"^/api/docs$",           # Allow Swagger UI
    r"^/api/openapi\.json$",  # Allow OpenAPI schema
    r"^/api/auth/.*$",        # Allow all paths starting with /auth/
]