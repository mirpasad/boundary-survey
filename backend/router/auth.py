from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from core.config import settings
from core.jwt import create_jwt

router = APIRouter(tags=["Auth"])

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/auth/token", response_model=TokenOut)
def login(request: LoginIn) -> TokenOut:
    # Simple dev login. Replace with real user store later.
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Missing headers")
    if request.email != settings.DEV_LOGIN_EMAIL or request.password != settings.DEV_LOGIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(
        subject=request.email,
        expires_in_seconds=settings.JWT_TTL_SECONDS,
        extra={"role": "developer"}  # add any custom claims you want
    )
    return TokenOut(access_token=token, expires_in=settings.JWT_TTL_SECONDS)