from pydantic import BaseModel, Field
from typing import Literal, List, Optional

# Pydantic schema definitions for survey generation and output.
# Used for request validation and response serialization in survey endpoints.

QuestionType = Literal["multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"]

class Question(BaseModel):
    type: QuestionType
    title: str = Field(min_length=1, max_length=500)
    options: Optional[List[str]] = None  

class SurveyOut(BaseModel):
    title: str
    description: Optional[str] = ""
    questions: List[Question]

class GenerateIn(BaseModel):
    description: str = Field(min_length=5, max_length=2000)
