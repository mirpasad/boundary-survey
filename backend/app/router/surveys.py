# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.schemas.generate import GenerateIn, SurveyOut
from app.core.rate_limit import limiter
from app.db.base import get_db
from app.db.models import CachedSurvey
from app.utils.hash import hash_prompt
from app.services.llm import generate_with_llm
from app.utils.validate import validate_string_length
from loguru import logger
import json
from app.core.config import settings

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
   # 1. Validate input content
    if not validate_string_length(body.description, min_length=5, max_length=2000):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input contains restricted content"
        )

    # # 2. Create hash key for caching
    # prompt_hash = hash_prompt(body.description)
    
    # # 3. Check cache
    # cached = db.query(CachedSurvey).filter(
    #     CachedSurvey.prompt_hash == prompt_hash
    # ).first()
    
    # if cached:
    #     logger.info("Returning cached survey")
    #     return json.loads(cached.survey_data)

   # 4. Generate new survey with LLM
    try:
        survey = generate_with_llm(body.description)
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Survey generation service unavailable"
        )
    
    print("lol survey", survey)

    # # 5. Validate LLM output structure
    # if not isinstance(survey, dict) or not survey.get("questions"):
    #     logger.error("Invalid survey structure from LLM")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Invalid survey format generated"
    #     )
        
    # # 6. Cache the new result
    # try:
    #     new_cache = CachedSurvey(
    #         prompt_hash=prompt_hash,
    #         survey_data=json.dumps(survey),
    #         prompt=body.description[:500]  # Store first 500 chars for reference
    #     )
    #     db.add(new_cache)
    #     db.commit()
    # except Exception as e:
    #     logger.warning(f"Caching failed: {str(e)}")
    #     # Don't fail the request if caching fails

    return survey

@router.get("/test")
def test():
    return {"message": "Hello World!"}