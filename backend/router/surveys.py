import asyncio
import json
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from schemas.generate import GenerateIn, SurveyOut
from core.rate_limit import limiter
from db.base import get_db
from db.models import CachedSurvey
from utils.hash import hash_prompt
from services.llm import generate_with_llm
from utils.validate import validate_string_length
from core.config import settings
from core.redis import redis_client

router = APIRouter(prefix="/surveys")

@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=SurveyOut,
    response_model_exclude_none=True,
)
@limiter.limit(settings.RATE_LIMIT)
async def generate(
    body: GenerateIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Generates a survey using LLM based on input description.
    Checks Redis and DB cache before generating a new survey.
    Caches results in both Redis and DB for future requests.
    """
    if not validate_string_length(body.description, min_length=5, max_length=2000):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input contains restricted content",
        )

    prompt_hash = hash_prompt(body.description)
    redis_key = f"survey:{prompt_hash}"

    # 1) Redis cache
    try:
        cached_data = await redis_client.get(redis_key)
        if cached_data:
            logger.info(f"Redis cache hit: {redis_key}")
            # decode bytes -> str -> dict
            return json.loads(cached_data.decode("utf-8"))
    except Exception as e:
        logger.warning(f"Redis get failed: {e}")

    # 2) DB cache (non-blocking read via executor)
    loop = asyncio.get_event_loop()
    try:
        cached_survey = await loop.run_in_executor(
            None,
            lambda: db.query(CachedSurvey)
                      .filter(CachedSurvey.prompt_hash == prompt_hash)
                      .first()
        )
        if cached_survey:
            logger.info(f"Database cache hit: {prompt_hash}")
            # Re-prime Redis (best-effort)
            try:
                await redis_client.setex(
                    redis_key,
                    settings.REDIS_CACHE_TTL,
                    cached_survey.payload
                )
            except Exception as e:
                logger.warning(f"Redis re-prime failed: {e}")
            return json.loads(cached_survey.payload)
    except Exception as e:
        logger.warning(f"DB read failed: {e}")

    # 3) Generate new survey with LLM
    try:
        survey = await generate_with_llm(body.description)  # FIX: await
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "LLM generation failed", "code": "LLM_ERROR"}},
        )

    # Basic shape validation (SurveyOut enforces further)
    if not isinstance(survey, dict) or not survey.get("questions"):
        logger.error("Invalid survey structure from LLM")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid survey format generated",
        )

    survey_json = json.dumps(survey)

    # 4) Cache in Redis with TTL (best-effort)
    try:
        await redis_client.setex(
            redis_key,
            settings.REDIS_CACHE_TTL,
            survey_json
        )
    except Exception as e:
        logger.warning(f"Redis caching failed: {str(e)}")

    # 5) Cache in DB (non-blocking, with retries)
    try:
        await loop.run_in_executor(
            None, lambda: cache_in_db(prompt_hash, body.description, survey_json, db)
        )
    except Exception as e:
        logger.warning(f"DB caching failed: {str(e)}")

    return survey

@router.get("/test")
def test():
    """Simple test endpoint for health checks."""
    return {"message": "Hello World!"}

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(0.5),
    retry=retry_if_exception_type(sqlalchemy.exc.OperationalError),
)
def cache_in_db(prompt_hash: str, description: str, survey_json: str, db: Session):
    """
    Synchronous DB caching function for executor.
    Retries on operational errors to improve reliability.
    """
    try:
        cache_entry = CachedSurvey(
            prompt_hash=prompt_hash,
            prompt=description,
            payload=survey_json
        )
        db.add(cache_entry)
        db.commit()
        logger.info(f"Cached in DB: {prompt_hash}")
    except Exception as e:
        db.rollback()
        logger.error(f"DB cache commit failed: {str(e)}")
