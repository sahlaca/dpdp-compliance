from __future__ import annotations

from typing import Any

from app.rag.retrieve import build_search_query, retrieve_citations
from app.rules.models import ComplianceStatus, ObligationResult
from app.rules.obligations import OBLIGATION_SOURCE_MAP, OBLIGATIONS
from app.rules.scoring import score_obligation

_STATUS_ORDER = {
    ComplianceStatus.NOT_MET: 0,
    ComplianceStatus.PARTIAL: 1,
    ComplianceStatus.NOT_ANSWERED: 2,
    ComplianceStatus.MET: 3,
    ComplianceStatus.NOT_APPLICABLE: 4,
}


def evaluate_obligations(answers: dict[str, Any]) -> list[ObligationResult]:
    results: list[ObligationResult] = []
    for item in OBLIGATIONS:
        status, gap, action = score_obligation(item["id"], answers)
        source_ids = OBLIGATION_SOURCE_MAP.get(item["id"], ["dpdp_act_2023", "dpdp_rules_2025"])
        query = build_search_query(item["act_sections"], item["rule_references"], item["title"])
        citations = retrieve_citations(query, source_ids=source_ids, top_k=2)

        results.append(
            ObligationResult(
                id=item["id"],
                title=item["title"],
                category=item["category"],
                status=status,
                act_sections=item["act_sections"],
                rule_references=item["rule_references"],
                deadline=item["deadline"],
                priority=item["priority"],
                description=item["description"],
                gap_summary=gap,
                recommended_action=action,
                source_ids=source_ids,
                citations=citations,
            )
        )

    results.sort(key=lambda r: (r.priority, _STATUS_ORDER[r.status], r.title))
    return results
