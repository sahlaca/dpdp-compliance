from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

TechnicalAnswer = Literal["yes", "partial", "no", "na"]

SCORE_LABELS = {
    "yes": "Yes — fully implemented, documented, and audited",
    "partial": "Partial — process exists but incomplete",
    "no": "No — not in place",
    "na": "N/A — not applicable to our business",
}

SCORE_POINTS = {
    "yes": 3,
    "partial": 1,
    "no": 0,
    "na": None,
}


class TechnicalQuestionOption(BaseModel):
    value: TechnicalAnswer
    label: str
    points: int | None = None


class TechnicalQuestion(BaseModel):
    id: str
    domain_id: str
    domain_name: str
    code: str
    prompt: str
    options: list[TechnicalQuestionOption]


class TechnicalDomain(BaseModel):
    id: str
    name: str
    number: int
    description: str


class TechnicalQuestionnaireResponse(BaseModel):
    version: str = "1.0.0"
    title: str = "The DPDP Act Client Gap Assessment Survey"
    scoring_criteria: list[str] = Field(
        default_factory=lambda: [
            "Yes — 3 points — fully implemented, documented, and audited",
            "Partial — 1 point — process exists but incomplete",
            "No — 0 points — not in place",
            "N/A — excluded from scoring — not applicable to your business",
        ]
    )
    domains: list[TechnicalDomain]
    questions: list[TechnicalQuestion]


class TechnicalSubmission(BaseModel):
    company_name: str = Field(..., min_length=1)
    sector: str = Field(default="other")
    answers: dict[str, Any] = Field(default_factory=dict)
