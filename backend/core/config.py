from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file at startup

import os
from pydantic import BaseModel

# Settings class centralizes all configuration for the backend service.
# Values are loaded from environment variables for flexibility and security.
# This approach supports production-grade practices such as environment-based config,
# secret management, and easy overrides for testing or deployment.
class Settings(BaseModel):
    # General environment and API configuration
    ENV: str = os.getenv("ENV", "local")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    # LLM service configuration
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL")

    # Database connection string
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://survey:survey@db:5432/surveys",
    )

    # Rate limiting and CORS settings
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "10/minute")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")  
    
    # JWT authentication configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_TTL_SECONDS: int = int(os.getenv("JWT_TTL_SECONDS"))

    # Developer login credentials (for development/testing only)
    DEV_LOGIN_EMAIL: str = os.getenv("DEV_LOGIN_EMAIL")
    DEV_LOGIN_PASSWORD: str = os.getenv("DEV_LOGIN_PASSWORD")
    
    # Redis cache configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT"))
    REDIS_CACHE_TTL: int = int(os.getenv("REDIS_CACHE_TTL"))
    
    # Cache strategy for data retrieval
    CACHE_STRATEGY: str = os.getenv("CACHE_STRATEGY", "redis_first")  # Options: "redis_first", "db_only", "redis_only"

    # Global request timeout for API endpoints
    GLOBAL_REQUEST_TIMEOUT: int = int(os.getenv("GLOBAL_REQUEST_TIMEOUT", 30))

# Instantiate settings for use throughout the application
settings = Settings()