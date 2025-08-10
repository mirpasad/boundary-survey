import os
import json
from urllib import response
from core.retryPolicy import RETRY_POLICY
import groq
from loguru import logger
from core.config import settings
import httpx

# This module integrates with the Groq LLM API to generate surveys from user descriptions.
# It applies a system prompt for survey design, validates output, and handles errors and retries.

client = groq.Groq(api_key=settings.GROQ_API_KEY)

@RETRY_POLICY
async def generate_with_llm(description: str) -> dict:
    """
    Generate a structured survey from a description using an LLM.
    Applies a system prompt and validates the output structure.
    """
    async with httpx.AsyncClient(timeout=settings.LLM_NETWORK_TIMEOUT) as client:
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
        USER_PROMPT = f"Survey description: {description}"

        try:
            # Call the LLM API and handle response
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
            # Handle rate limit and server errors
            if response.status_code == 429:
                logger.warning("Rate limited by Groq API")
                raise httpx.HTTPStatusError("Rate limited", request=response.request, response=response)
            elif response.status_code >= 500:
                logger.error(f"Groq server error: {response.status_code}")
                raise httpx.HTTPStatusError("Server error", request=response.request, response=response)

            # Parse and validate JSON response
            json_str = response.choices[0].message.content
            survey_data = json.loads(json_str)
            if validate_survey_structure(survey_data):
                return survey_data
            else:
                logger.error(f"LLM returned invalid structure: {json_str}")
                raise ValueError("Invalid LLM response structure")

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise e

def validate_survey_structure(data: dict) -> bool:
    """
    Validate LLM output matches SurveyOut schema.
    Checks required fields and type-specific question structure.
    """
    required_keys = {"title", "questions"}
    question_required = {"type", "question"}
    type_specific = {
        "multiple_choice": {"options"},
        "rating_scale": {"min", "max"},
        "open_text": set(),
        "ranking": {"items"},
        "boolean": set()
    }
    if not all(key in data for key in required_keys):
        return False
    for q in data.get("questions", []):
        if not all(k in q for k in question_required):
            return False
        q_type = q["type"]
        if q_type not in type_specific:
            return False
        if not all(k in q for k in type_specific[q_type]):
            return False
    return True