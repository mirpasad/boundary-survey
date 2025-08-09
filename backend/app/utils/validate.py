from app.schemas.generate import SurveyOut

def validate_string_length(text: str, min_length: int, max_length: int) -> bool:
    if not text:
        return False
    text_length = len(text)
    return min_length <= text_length <= max_length