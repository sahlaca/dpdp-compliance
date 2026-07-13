from datetime import datetime, timezone

from app.reports.questionnaire_summary import build_questionnaire_responses
from app.questionnaire.schema import QuestionnaireSubmission
from app.rules.engine import evaluate_obligations
from app.rules.models import ComplianceStatus
from app.sources.catalog import get_catalog

OBLIGATION_EXPLAINER = (
    "What is an obligation? A specific legal requirement under India's Digital Personal Data "
    "Protection Act 2023 and Rules 2025 — for example, publishing a privacy notice, obtaining "
    "valid consent, or appointing a grievance officer. The questionnaire asks about your "
    "business practices; this report shows which requirements apply to you and whether you meet them."
)

OBLIGATION_ASSESSMENT_INTRO = (
    "Obligations assessed from your answers. Items marked Not Answered need questionnaire input."
)

OBLIGATION_RELATIONSHIP_NOTE = (
    "Questions and obligations are separate: several questions can inform one obligation, "
    "and one obligation may need answers to multiple questions."
)

OBLIGATION_FIELD_LEGEND = {
    "title": "For each obligation below:",
    "items": [
        {"label": "Requirement", "description": "What does the law say?"},
        {"label": "Assessment", "description": "Where do we stand?"},
        {"label": "Recommended Action", "description": "What should we do now?"},
    ],
}


def build_legal_executive_overview(
    company: str,
    *,
    obligations_in_scope: int,
    obligations_assessed: int,
    gaps_found: int,
    critical_gaps: int,
    obligations_pending: int,
) -> str:
    """Narrative executive overview for the legal gap report."""
    opening = (
        f"{company} was assessed against applicable Data Fiduciary obligations under India's "
        "Digital Personal Data Protection Act, 2023 and the DPDP Rules, 2025. This legal "
        "compliance assessment maps your questionnaire responses to statutory requirements "
        "and identifies where practices meet, partially meet, or fall short of those obligations."
    )

    if obligations_in_scope == 0:
        findings = (
            "No applicable obligations were identified from the responses provided. "
            "Review your questionnaire answers or consult counsel if this result is unexpected."
        )
    elif obligations_pending:
        findings = (
            f"Of {obligations_in_scope} obligations in scope, {obligations_assessed} could be "
            f"assessed from your answers and {obligations_pending} remain pending further input. "
            f"{gaps_found} gap{'s' if gaps_found != 1 else ''} were identified"
        )
        if critical_gaps:
            findings += f", including {critical_gaps} critical item{'s' if critical_gaps != 1 else ''} marked Not Met."
        else:
            findings += "."
    else:
        findings = (
            f"Of {obligations_in_scope} obligations in scope, {obligations_assessed} were assessed "
            f"from your answers. {gaps_found} gap{'s' if gaps_found != 1 else ''} were identified"
        )
        if critical_gaps:
            findings += (
                f", including {critical_gaps} critical item{'s' if critical_gaps != 1 else ''} "
                "marked Not Met that warrant immediate attention."
            )
        elif gaps_found:
            findings += " requiring remediation or clarification."
        else:
            findings += (
                ". No material gaps were identified from the answers provided — continue monitoring "
                "regulatory updates and maintain current controls."
            )

    closing = (
        "The prioritized action plan, regulatory timeline, and detailed obligation assessment "
        "below set out recommended next steps ahead of the November 2026 and May 2027 compliance milestones."
    )

    return f"{opening}\n\n{findings} {closing}"


def generate_gap_report(submission: QuestionnaireSubmission) -> dict:
    all_obligations = evaluate_obligations(submission.answers)
    obligations = [
        o for o in all_obligations if o.status != ComplianceStatus.NOT_APPLICABLE
    ]
    questionnaire_responses = build_questionnaire_responses(submission.answers)
    catalog = get_catalog()

    gaps = [
        o
        for o in obligations
        if o.status in (ComplianceStatus.NOT_MET, ComplianceStatus.PARTIAL)
    ]
    not_met = [o for o in obligations if o.status == ComplianceStatus.NOT_MET]
    not_answered = [o for o in obligations if o.status == ComplianceStatus.NOT_ANSWERED]
    assessed = [o for o in obligations if o.status != ComplianceStatus.NOT_ANSWERED]

    questions_answered = sum(1 for q in questionnaire_responses if q["answered"])
    questions_total = len(questionnaire_responses)
    obligations_assessed = len(assessed)
    obligations_pending = len(not_answered)
    obligations_in_scope = len(obligations)

    # Collect unique source IDs referenced across obligations
    referenced_source_ids: set[str] = set()
    for o in obligations:
        referenced_source_ids.update(o.source_ids)
        for c in o.citations:
            referenced_source_ids.add(c["source_id"])

    sources_for_report = [
        s.model_dump()
        for s in catalog.sources
        if s.id in referenced_source_ids or s.type == "primary"
    ]

    action_plan = [
        {
            "phase": "Before Nov 13, 2026",
            "deadline": "2026-11-13",
            "items": [
                "Review Consent Manager provisions and whether registration applies to your use case",
                "Assess and update vendor / Data Processor contracts",
                "Publish or update privacy notice with grievance officer contact",
            ],
        },
        {
            "phase": "Before May 13, 2027 (full compliance)",
            "deadline": "2027-05-13",
            "items": [o.recommended_action for o in not_met] or ["Maintain current controls and monitor regulatory updates"],
        },
    ]

    executive_overview = build_legal_executive_overview(
        submission.company_name,
        obligations_in_scope=obligations_in_scope,
        obligations_assessed=obligations_assessed,
        gaps_found=len(gaps),
        critical_gaps=len(not_met),
        obligations_pending=obligations_pending,
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assessment_type": "legal",
        "company_name": submission.company_name,
        "sector": submission.sector,
        "summary": {
            "total_obligations": obligations_assessed,
            "obligations_assessed": obligations_assessed,
            "gaps_found": len(gaps),
            "critical_gaps": len(not_met),
            "questions_total": questions_total,
            "questions_answered": questions_answered,
            "questions_not_answered": questions_total - questions_answered,
            "obligations_not_answered": obligations_pending,
            "obligations_in_scope": obligations_in_scope,
        },
        "executive_overview": executive_overview,
        "obligation_explainer": OBLIGATION_EXPLAINER,
        "obligation_assessment_intro": OBLIGATION_ASSESSMENT_INTRO,
        "obligation_relationship_note": OBLIGATION_RELATIONSHIP_NOTE,
        "obligation_field_legend": OBLIGATION_FIELD_LEGEND,
        "regulatory_timeline": [p.model_dump() for p in catalog.implementation_phases],
        "legal_sources": sources_for_report,
        "questionnaire_responses": questionnaire_responses,
        "obligations": [o.model_dump() for o in obligations],
        "prioritized_action_plan": action_plan,
        "disclaimer": (
            "This report is automated compliance guidance based on your questionnaire answers "
            "and the DPDP Act 2023 / DPDP Rules 2025. It is not legal advice. "
            "Download and verify the cited source documents below. "
            "Consult qualified counsel before relying on this report for regulatory decisions."
        ),
    }
