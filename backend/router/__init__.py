from .auth import router as auth_router
from .surveys import router as surveys_router

routers = [
  auth_router,
  surveys_router
]