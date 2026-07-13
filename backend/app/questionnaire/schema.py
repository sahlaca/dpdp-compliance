from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    TEXT = "text"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    BOOLEAN = "boolean"
    NUMBER = "number"


class QuestionOption(BaseModel):
    value: str
    label: str


class Question(BaseModel):
    id: str
    section: str
    prompt: str
    help_text: Optional[str] = None
    type: QuestionType
    required: bool = True
    options: Optional[List[QuestionOption]] = None


class QuestionnaireResponse(BaseModel):
    version: str = "0.1.0"
    sections: list[str]
    sectors: list[QuestionOption]
    questions: list[Question]


class QuestionnaireSubmission(BaseModel):
    company_name: str = Field(..., min_length=1)
    sector: str = Field(..., description="e.g. hospitality, retail, healthcare, d2c")
    answers: dict[str, Any] = Field(default_factory=dict)
