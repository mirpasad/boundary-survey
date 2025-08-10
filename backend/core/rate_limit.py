from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limiting configuration for the backend API.
# Uses SlowAPI to limit requests based on the client's remote address.
limiter = Limiter(key_func=get_remote_address)
