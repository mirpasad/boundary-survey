from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from core.config import settings

# This module provides utility functions for creating, verifying, and decoding JWT tokens.
# It uses configuration from settings for secret and algorithm, supporting secure authentication.


def create_token(data):
    # Create a JWT token using static secret and HS256 algorithm (legacy/test use)
    return jwt.encode(data, "secret", algorithm="HS256")


def verify_token(token):
    # Decode and verify a JWT token using static secret and HS256 algorithm (legacy/test use)
    return jwt.decode(token, "secret", algorithms=["HS256"])


def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT using production configuration.
    Requires 'exp' and 'iat' claims and verifies signature."""
    options = {"require": ["exp", "iat"], "verify_signature": True}
    kwargs: Dict[str, Any] = {
        "algorithms": [settings.JWT_ALGORITHM],
        "options": options,
    }
    return jwt.decode(token, settings.JWT_SECRET, **kwargs)


def create_jwt(
    subject: str,
    expires_in_seconds: int = 3600,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT for a given subject, with expiration and optional extra claims.
    Used for authentication and testing."""
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in_seconds)).timestamp()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)