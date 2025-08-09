from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.schemas.generate import GenerateIn, SurveyOut
from app.core.security import require_api_key
from app.core.rate_limit import limiter
from app.db.base import get_db, Base, engine
from app.db.models import CachedSurvey
from app.utils.hash import hash_prompt
from app.services.llm import generate_with_llm
import json

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

@router.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)

@router.post("/surveys/generate", response_model=SurveyOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def generate(body: GenerateIn, request: Request, _=Depends(require_api_key), db: Session = Depends(get_db)):
    h = hash_prompt(body.description)
    cached = db.query(CachedSurvey).filter(CachedSurvey.prompt_hash == h).first()
    if cached:
        return json.loads(cached.payload)

    payload = await generate_with_llm(body.description)
    # basic normalization: ensure options exist only for choice types
    for q in payload.get("questions", []):
        t = q.get("type")
        if t not in {"multipleChoice","singleChoice"}:
            q.pop("options", None)

    survey_json = json.dumps(payload)
    db.add(CachedSurvey(prompt_hash=h, prompt=body.description, payload=survey_json))
    db.commit()
    return payload
