# import os, json, httpx
# from app.core.config import settings

# FALLBACK = {
#   "title": "Customer Feedback Survey",
#   "description": "Quick pulse on satisfaction, issues and ideas.",
#   "questions": [
#     {"type": "singleChoice", "title": "Overall, how satisfied are you?", "options": ["Very satisfied", "Somewhat", "Not satisfied"]},
#     {"type": "multipleChoice", "title": "Which areas need improvement?", "options": ["Checkout", "Search", "Support", "Delivery"]},
#     {"type": "shortAnswer", "title": "One thing we could do better:"},
#     {"type": "scale", "title": "Rate the website experience (1–10)"},
#   ]
# }

# async def generate_with_llm(prompt: str) -> dict:
#     if not settings.GROQ_API_KEY:
#         return FALLBACK

#     spec = """
# Return ONLY JSON with keys: title, description, questions.
# Each question: {type, title, options?}
# type must be one of ["multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"].
# Generate 4–8 useful questions. Options only for choice types. English.
# """
#     body = {
#         "model": settings.GROQ_MODEL,
#         "input": f"Description: {prompt}\n\n{spec}",
#         "response_format": {"type": "json_object"},
#     }
#     headers = {
#         "Authorization": f"Bearer {settings.GROQ_API_KEY}",
#         "Content-Type": "application/json",
#     }
#     async with httpx.AsyncClient(timeout=30) as client:
#         r = await client.post("https://api.openai.com/v1/responses", json=body, headers=headers)
#         r.raise_for_status()
#         data = r.json()
#         text = data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
#         try:
#             return json.loads(text)
#         except Exception:
#             return FALLBACK


# app/services/llm.py
import os
import json
from urllib import response
import groq
# from openai import OpenAI
from loguru import logger
from app.core.config import settings

# Initialize OpenAI client
client = groq.Groq(api_key=settings.GROQ_API_KEY)

def generate_with_llm(description: str) -> dict:
    """
    Generate a structured survey from a description using an LLM
    
    Args:
        description: User's survey description (e.g., "Customer satisfaction for an online store")
    
    Returns:
        Dictionary matching SurveyOut schema
    """
    # System prompt to guide the LLM
    SYSTEM_PROMPT = """
    You are an expert survey designer. Create a comprehensive survey based on the user's description.
    
    Output Requirements:
    1. Return valid JSON with this structure:
        {
            "title": "Survey Title",
            "description": "Survey overview",
            "questions": [
                {
                    "type": "question_type",
                    "question": "Question text",
                    ...type-specific fields
                }
            ]
        }
    
    2. Question types and required fields:
        - multiple_choice: {options: [list of choices], allow_multiple: bool}
        - rating_scale: {min: 1, max: number(5/7/10), min_label: "Poor", max_label: "Excellent"}
        - open_text: {multiline: bool}
        - ranking: {items: [list to rank]}
        - boolean: {}
    
    3. Guidelines:
        - Include 5-8 questions covering all relevant aspects
        - Mix question types appropriately
        - Ensure questions are neutral and unbiased
        - Add a title that summarizes the survey
        - Include a brief description explaining the survey's purpose
    """

    # User prompt with the actual description
    USER_PROMPT = f"Survey description: {description}"

    try:
        # Call the LLM API
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ],
            temperature=0.3,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )
        
        print("lol response", response)

        # Extract and parse JSON response
        json_str = response.choices[0].message.content
        survey_data = json.loads(json_str)

        print("lol survey_data", survey_data)

        # Validate structure before returning
        if validate_survey_structure(survey_data):
            return survey_data
        else:
            logger.error(f"LLM returned invalid structure: {json_str}")
            return generate_fallback_survey(description)
            
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        return generate_fallback_survey(description)

def generate_fallback_survey(description: str) -> dict:
    """Generate a basic survey when LLM fails"""
    return {
        "title": f"Survey: {description[:50]}",
        "description": "This survey was automatically generated",
        "questions": [
            {
                "type": "rating_scale",
                "question": "Overall satisfaction",
                "min": 1,
                "max": 5,
                "min_label": "Very Dissatisfied",
                "max_label": "Very Satisfied"
            },
            {
                "type": "multiple_choice",
                "question": "What was your most important reason for choosing our service?",
                "options": ["Price", "Quality", "Convenience", "Reputation", "Other"],
                "allow_multiple": False
            },
            {
                "type": "open_text",
                "question": "Additional comments or suggestions",
                "multiline": True
            }
        ]
    }
    
    
def validate_survey_structure(data: dict) -> bool:
    """Validate LLM output matches SurveyOut schema"""
    required_keys = {"title", "questions"}
    question_required = {"type", "question"}
    type_specific = {
        "multiple_choice": {"options"},
        "rating_scale": {"min", "max"},
        "open_text": set(),
        "ranking": {"items"},
        "boolean": set()
    }
    
    # Check top-level structure
    if not all(key in data for key in required_keys):
        return False
    
    # Validate each question
    for q in data.get("questions", []):
        if not all(k in q for k in question_required):
            return False
        
        # Validate type-specific fiFelds
        q_type = q["type"]
        if q_type not in type_specific:
            return False
        if not all(k in q for k in type_specific[q_type]):
            return False
    
    return True