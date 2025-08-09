import os, json, httpx
from app.core.config import settings

FALLBACK = {
  "title": "Customer Feedback Survey",
  "description": "Quick pulse on satisfaction, issues and ideas.",
  "questions": [
    {"type": "singleChoice", "title": "Overall, how satisfied are you?", "options": ["Very satisfied", "Somewhat", "Not satisfied"]},
    {"type": "multipleChoice", "title": "Which areas need improvement?", "options": ["Checkout", "Search", "Support", "Delivery"]},
    {"type": "shortAnswer", "title": "One thing we could do better:"},
    {"type": "scale", "title": "Rate the website experience (1–10)"},
  ]
}

async def generate_with_llm(prompt: str) -> dict:
    if not settings.OPENAI_API_KEY:
        return FALLBACK

    spec = """
Return ONLY JSON with keys: title, description, questions.
Each question: {type, title, options?}
type must be one of ["multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"].
Generate 4–8 useful questions. Options only for choice types. English.
"""
    body = {
        "model": settings.OPENAI_MODEL,
        "input": f"Description: {prompt}\n\n{spec}",
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post("https://api.openai.com/v1/responses", json=body, headers=headers)
        r.raise_for_status()
        data = r.json()
        # responses API: output[0].content[0].text
        text = data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
        try:
            return json.loads(text)
        except Exception:
            return FALLBACK
