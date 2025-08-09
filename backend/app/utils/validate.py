from app.schemas.generate import SurveyOut

def validate_payload(payload: dict) -> dict:
    SurveyOut.model_validate(payload)
    return payload
