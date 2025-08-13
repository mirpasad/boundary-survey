import os
import asyncio
import json
from urllib import response
from core.retryPolicy import RETRY_POLICY
import groq
from loguru import logger
from core.config import settings
import httpx

# This module integrates with the Groq LLM API to generate surveys from user descriptions.
# It applies a system prompt for survey design, validates output, and handles errors and retries.

groq_client = groq.Groq(api_key=settings.GROQ_API_KEY)

# IMPORTANT: We align the LLM output to our Pydantic schema in schemas/generate.py.
SYSTEM_PROMPT = """
You are an expert survey designer.

Return ONLY valid JSON (no markdown fences, no commentary) matching exactly this schema:

{
  "title": "string (survey title)",
  "description": "string (optional, brief summary of the survey)",
  "questions": [
    {
      "type": "multipleChoice" | "singleChoice" | "openQuestion" | "shortAnswer" | "scale" | "npsScore",
      "title": "string (question text)",
      "options": ["string", "..."]  // include only for choice-based questions; omit otherwise
    }
  ]
}

Rules:
- Provide 5 to 8 questions, neutral and unbiased.
- Use 'multipleChoice' when multiple answers make sense; 'singleChoice' when only one should be selected.
- For 'scale', assume a 1–10 scale implicitly; do not add min/max fields.
- For 'npsScore', use standard 0–10 intent but return only the question 'title' (no extra fields).
- Do NOT include any fields other than the ones defined in the schema above.
- Output MUST be a single JSON object.
"""

def _call_groq(description: str) -> dict:
    resp = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Survey description: {description}"}
        ],
        temperature=0.3,
        max_tokens=1200,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    return json.loads(content)

def _validate_against_schema_like(data: dict) -> bool:
    # Lightweight structural validation aligned to schemas/generate.py (Option A)
    if not isinstance(data, dict): return False
    if "title" not in data or "questions" not in data: return False
    if not isinstance(data["questions"], list) or len(data["questions"]) == 0: return False

    allowed_types = {"multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"}
    for q in data["questions"]:
        if not isinstance(q, dict): return False
        if "type" not in q or "title" not in q: return False
        if q["type"] not in allowed_types: return False
        if "options" in q and not isinstance(q["options"], list): return False
    return True

@RETRY_POLICY
async def generate_with_llm(description: str) -> dict:
    """
    Calls Groq to generate a survey JSON matching our schemas.generate.SurveyOut contract.
    Wrapped in a retry policy; executed in a thread to avoid blocking the event loop.
    """
    loop = asyncio.get_event_loop()
    try:
        # Run the (blocking) SDK call in a thread, with a soft timeout at the request layer.
        data = await loop.run_in_executor(None, lambda: _call_groq(description))
        if not _validate_against_schema_like(data):
            logger.error(f"LLM returned invalid structure: {data}")
            raise ValueError("Invalid LLM response structure")
        return data
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise