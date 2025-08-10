from schemas.generate import SurveyOut

# Utility function for validating the length of a string.
# Used to ensure survey descriptions and other inputs meet length requirements.
def validate_string_length(text: str, min_length: int, max_length: int) -> bool:
    if not text:
        return False
    text_length = len(text)
    return min_length <= text_length <= max_length