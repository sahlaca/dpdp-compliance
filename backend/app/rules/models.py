from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ComplianceStatus(str, Enum):
    MET = "met"
    PARTIAL = "partial"
    NOT_MET = "not_met"
    NOT_ANSWERED = "not_answered"
    NOT_APPLICABLE = "not_applicable"


class ObligationResult(BaseModel):
    id: str
    title: str
    category: str
    status: ComplianceStatus
    act_sections: list[str]
    rule_references: list[str]
    deadline: str
    priority: int
    description: str
    gap_summary: str
    recommended_action: str
    source_ids: list[str] = []
    citations: list[dict[str, Any]] = []
