# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.schemas.generate import GenerateIn, SurveyOut
from app.core.rate_limit import limiter
from app.db.base import get_db
from app.db.models import CachedSurvey
from app.utils.hash import hash_prompt
from app.services.llm import generate_with_llm
from app.utils.validate import validate_payload
from loguru import logger
import json
from app.core.config import settings

router = APIRouter()

@router.post(
    "/surveys/generate",
    response_model=SurveyOut,
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
    h = hash_prompt(body.description)

    cached = db.query(CachedSurvey).filter(CachedSurvey.prompt_hash == h).first()
    if cached:
        logger.info("cache_hit prompt='{}'", body.description)
        response.status_code = status.HTTP_200_OK
        return json.loads(cached.payload)

    payload = await generate_with_llm(body.description)

    for q in payload.get("questions", []):        
        if q.get("type") not in {"multipleChoice", "singleChoice"}:
            q.pop("options", None)

    payload = validate_payload(payload)

    db.add(CachedSurvey(prompt_hash=h, prompt=body.description, payload=json.dumps(payload)))
    db.commit()
    return payload
