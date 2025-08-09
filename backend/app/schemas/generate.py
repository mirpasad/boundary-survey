from pydantic import BaseModel, Field
from typing import Literal, List, Optional

QuestionType = Literal["multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"]

class Question(BaseModel):
    type: QuestionType
    title: str = Field(min_length=1, max_length=500)
    options: Optional[List[str]] = None  # only for choice types

class SurveyOut(BaseModel):
    title: str
    description: Optional[str] = ""
    questions: List[Question]

class GenerateIn(BaseModel):
    description: str = Field(min_length=5, max_length=2000)
