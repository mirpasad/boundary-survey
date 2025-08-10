from .auth import router as auth_router
from .surveys import router as surveys_router

# Aggregates all API routers for the backend service.
# This allows easy inclusion of authentication and survey routes in the main application.
routers = [
  auth_router,
  surveys_router
]