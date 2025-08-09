publicPaths = [
  r"^/health$",  # Exact match for /health
    r"^/public/.*$",  # Allow all paths starting with /public/
    r"^/$",  # Allow root path
    r"^/docs$",  # Allow Swagger UI
    r"^/openapi\.json$",  # Allow OpenAPI schema
    r"^/auth/.*$",  # Allow all paths starting with /auth/
]