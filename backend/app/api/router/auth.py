from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.core.config import settings
from app.core.jwt import create_jwt

router = APIRouter(tags=["auth"])

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/auth/token", response_model=TokenOut)
def login(body: LoginIn):
    # Simple dev login. Replace with real user store later.
    if body.email != settings.DEV_LOGIN_EMAIL or body.password != settings.DEV_LOGIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_jwt(
        subject=body.email,
        expires_in_seconds=settings.JWT_TTL_SECONDS,
        extra={"role": "developer"}  # add any custom claims you want
    )
    return TokenOut(access_token=token, expires_in=settings.JWT_TTL_SECONDS)
