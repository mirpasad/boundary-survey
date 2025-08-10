# app/api/routes.py
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
import sqlalchemy
from sqlalchemy.orm import Session
from schemas.generate import GenerateIn, SurveyOut
from core.rate_limit import limiter
from db.base import get_db
from db.models import CachedSurvey
from utils.hash import hash_prompt
from services.llm import generate_with_llm
from utils.validate import validate_string_length
from loguru import logger
import json
from core.config import settings
from core.redis import redis_client
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from starlette.responses import JSONResponse

# Survey router handles endpoints for survey generation and caching.
# Implements multi-layer caching (Redis, DB) and integrates with LLM service.
router = APIRouter(prefix="/surveys")

@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
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
            detail="Input contains restricted content"
        )

    prompt_hash = hash_prompt(body.description)
    redis_key = f"survey:{prompt_hash}"

    # Check Redis cache first
    cached_data = await redis_client.get(redis_key)
    if cached_data:
        logger.info(f"Redis cache hit: {redis_key}")
        return json.loads(cached_data)
    
    # Check database cache
    cached_survey = db.query(CachedSurvey).filter(
        CachedSurvey.prompt_hash == prompt_hash
    ).first()
    if cached_survey:
        logger.info(f"Database cache hit: {prompt_hash}")
        await redis_client.setex(
            redis_key,
            settings.REDIS_CACHE_TTL,
            cached_survey.payload
        )
        return json.loads(cached_survey.payload)

    # Generate new survey with LLM
    try:
        survey = generate_with_llm(body.description)
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,  # Internal Server Error
            content={"error": {
                "message": "LLM generation failed",
                "code": "LLM_ERROR"
            }}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Survey generation service unavailable"
        )

    # Validate LLM output structure
    if not isinstance(survey, dict) or not survey.get("questions"):
        logger.error("Invalid survey structure from LLM")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid survey format generated"
        )
    
    survey_json = json.dumps(survey)
    
    # Cache in Redis with TTL
    try:
        await redis_client.setex(
            redis_key,
            settings.REDIS_CACHE_TTL,
            survey_json
        )
    except Exception as e:
        logger.warning(f"Redis caching failed: {str(e)}")
        
    # Cache in database (async to avoid blocking)
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, 
            lambda: cache_in_db(prompt_hash, body.description, survey_json, db)
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
    retry=retry_if_exception_type(sqlalchemy.exc.OperationalError)
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
