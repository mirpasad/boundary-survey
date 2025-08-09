import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    ENV: str = os.getenv("ENV", "local")
    API_PREFIX: str = "/api"
    API_TOKEN: str = os.getenv("API_TOKEN", "dev-token-123")

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://survey:survey@db:5432/surveys",
    )

    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "10/minute")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")  # comma-separated

settings = Settings()
