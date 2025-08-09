from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from app.core.config import settings


def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode & validate a JWT using configured settings."""
    options = {"require": ["exp", "iat"], "verify_signature": True}
    kwargs: Dict[str, Any] = {
        "algorithms": [settings.JWT_ALGORITHM],
        "options": options,
    }
    if settings.JWT_ISSUER:
        kwargs["issuer"] = settings.JWT_ISSUER
    if settings.JWT_AUDIENCE:
        kwargs["audience"] = settings.JWT_AUDIENCE
    return jwt.decode(token, settings.JWT_SECRET, **kwargs)


def create_jwt(
    subject: str,
    expires_in_seconds: int = 3600,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """Helper for tests/tools to mint a token."""
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in_seconds)).timestamp()),
    }
    if settings.JWT_ISSUER:
        payload["iss"] = settings.JWT_ISSUER
    if settings.JWT_AUDIENCE:
        payload["aud"] = settings.JWT_AUDIENCE
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
