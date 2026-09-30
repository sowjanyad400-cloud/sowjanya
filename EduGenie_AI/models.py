from typing import Any, List, Optional

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    answer: Optional[str] = None
    explanation: Optional[str] = None
    summary: Optional[str] = None
    recommendations: Optional[Any] = None
    quiz: Optional[Any] = None


class ErrorResponse(BaseModel):
    detail: str


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question asked by the learner"
    )


class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        description="Topic that needs a simple explanation"
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Topic or educational passage for quiz generation"
    )


class SummaryRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Text to summarize"
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        description="Topic for the learning path"
    )

    level: str = Field(
        default="beginner",
        description="Learner level"
    )

    goal: Optional[str] = Field(
        default=None,
        description="Optional learning goal"
    )


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None