from dotenv import load_dotenv
load_dotenv()

import os
from pydantic import BaseModel

class Settings(BaseModel):
    ENV: str = os.getenv("ENV", "local")
    API_PREFIX: str = "/api"
    API_TOKEN: str = os.getenv("API_TOKEN", "dev-token-123")

    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://survey:survey@db:5432/surveys",
    )

    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "10/minute")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")  
    
     # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_TTL_SECONDS: int = int(os.getenv("JWT_TTL_SECONDS"))

    DEV_LOGIN_EMAIL: str = os.getenv("DEV_LOGIN_EMAIL")
    DEV_LOGIN_PASSWORD: str = os.getenv("DEV_LOGIN_PASSWORD")

settings = Settings()