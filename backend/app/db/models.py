from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, String, DateTime, func
from app.db.base import Base

class CachedSurvey(Base):
    __tablename__ = "cached_surveys"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)  # JSON as text (use JSONB if you prefer)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
