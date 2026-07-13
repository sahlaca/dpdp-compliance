from __future__ import annotations

from datetime import datetime, timezone

from app.technical.gap_content import (
    CONCLUSION_TEMPLATE,
    GAP_NARRATIVES,
    NEXT_STEP,
    REMEDIATION_PHASES,
)
from app.technical.questions import _QUESTIONS, SERVICE_OPPORTUNITIES
from app.technical.schema import SCORE_POINTS, TechnicalSubmission


def _status_label(compliance_pct: float) -> str:
    if compliance_pct >= 75:
        return "Healthy"
    if compliance_pct >= 50:
        return "Warning"
    return "Critical"


def _risk_level(overall_pct: float) -> str:
    if overall_pct >= 75:
        return "LOW RISK"
    if overall_pct >= 50:
        return "MODERATE RISK"
    return "HIGH RISK"


def _split_domains_by_status(domains_out: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    critical = [d for d in domains_out if d["status"] == "Critical"]
    warning = [d for d in domains_out if d["status"] == "Warning"]
    healthy = [d for d in domains_out if d["status"] == "Healthy"]
    return critical, warning, healthy


def _format_domain_list(domains: list[dict]) -> str:
    if not domains:
        return ""
    parts = [f"{d['number']}. {d['name']}" for d in domains]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def _domain_status_narrative(critical: list[dict], warning: list[dict]) -> str:
    """Narrative aligned to the domain breakdown table status labels."""
    if critical and warning:
        return (
            f" Critical status in {_format_domain_list(critical)}; "
            f"warning-level gaps in {_format_domain_list(warning)}."
        )
    if critical:
        return f" Critical status in {_format_domain_list(critical)}."
    if warning:
        return f" Warning-level gaps in {_format_domain_list(warning)}."
    return " All assessed domains are at healthy compliance levels."


def _executive_overview(
    company: str,
    overall_pct: int,
    risk_level: str,
    critical: list[dict],
    warning: list[dict],
) -> str:
    domain_note = _domain_status_narrative(critical, warning)
    if critical:
        domain_note += " Immediate remediation is recommended for critical domains."
    elif warning:
        domain_note += " Targeted improvement is recommended to reach full compliance."

    return (
        f"{company} recently underwent a comprehensive gap analysis to evaluate its current data processing, "
        "storage, and application architecture against the statutory requirements of India's Digital Personal "
        "Data Protection (DPDP) Act.\n\n"
        "As the Data Protection Board of India (DPBI) enforces strict regulations backed by significant "
        "financial penalties (up to ₹250 Crore per major breach), this assessment establishes a baseline of "
        f"your organizational risk and outlines the technical and structural remediation steps required to "
        f"achieve compliance.\n\n"
        f"Current Compliance Rating: {overall_pct}% ({risk_level})."
        f"{domain_note}"
    )


def _scorecard_note(
    overall_pct: int,
    risk_level: str,
    critical: list[dict],
    warning: list[dict],
) -> str:
    if not critical and not warning:
        return (
            f"Status: Overall compliance is at {overall_pct}% ({risk_level}). "
            "Continue strengthening controls and re-assess after material infrastructure changes."
        )

    status_text = _domain_status_narrative(critical, warning).strip()
    if critical:
        suffix = " Immediate attention is required for domains rated Critical (<50% compliance)."
    else:
        suffix = " Remediation is recommended for domains rated Warning (50–74% compliance)."
    return f"Status: {status_text}{suffix}"


def _build_critical_gaps(responses: list[dict], question_map: dict) -> list[dict]:
    gaps: list[dict] = []
    for r in responses:
        if r.get("answer") != "no":
            continue
        q = question_map[r["id"]]
        narrative = GAP_NARRATIVES.get(q.id, {})
        gaps.append(
            {
                "id": q.id,
                "code": q.code,
                "domain": q.domain_name,
                "domain_number": int(q.domain_id.split("_")[1]),
                "title": narrative.get("title", q.prompt.split(":")[0] if ":" in q.prompt else q.code),
                "prompt": q.prompt,
                "gap": narrative.get(
                    "gap",
                    "This control is not in place based on your assessment response.",
                ),
                "legal_risk": narrative.get(
                    "legal_risk",
                    "Non-compliance with this control may increase exposure under the DPDP Act and Rules.",
                ),
                "recommended_service": narrative.get(
                    "recommended_service",
                    SERVICE_OPPORTUNITIES.get(q.domain_id, ""),
                ),
            }
        )
    return gaps[:5]


def _build_remediation(company: str, failing_domains: list[dict]) -> list[dict]:
    phases = []
    for template in REMEDIATION_PHASES:
        phase = dict(template)
        phase["items"] = list(template["deliverables"])  # backward compat
        phases.append(phase)

    if failing_domains:
        domain_items = [
            f"Address Domain {d['number']} ({d['name']}): {d['service_opportunity']}"
            for d in sorted(failing_domains, key=lambda x: x["compliance_pct"])
        ]
        phases[-1]["deliverables"] = list(phases[-1]["deliverables"]) + domain_items[:3]
        phases[-1]["items"] = phases[-1]["deliverables"]

    phases.append(
        {
            "phase": "Conclusion & Next Steps",
            "timeline": "Immediate",
            "summary": CONCLUSION_TEMPLATE.format(company=company),
            "deliverables": [NEXT_STEP],
            "items": [NEXT_STEP],
        }
    )
    return phases


def generate_technical_report(submission: TechnicalSubmission) -> dict:
    answers = submission.answers
    question_map = {q.id: q for q in _QUESTIONS}

    domain_results: dict[str, dict] = {}
    for q in _QUESTIONS:
        if q.domain_id not in domain_results:
            domain_results[q.domain_id] = {
                "id": q.domain_id,
                "name": q.domain_name,
                "number": int(q.domain_id.split("_")[1]),
                "score": 0,
                "max_points": 0,
                "questions": [],
            }

    responses = []
    for q in _QUESTIONS:
        raw = answers.get(q.id)
        answer = raw if raw in SCORE_POINTS else None
        points = SCORE_POINTS.get(answer) if answer else None
        applicable = answer is not None and answer != "na"

        if applicable:
            domain_results[q.domain_id]["max_points"] += 3
            domain_results[q.domain_id]["score"] += points or 0

        answer_label = {
            "yes": "Yes (3 points)",
            "partial": "Partial (1 point)",
            "no": "No (0 points)",
            "na": "N/A — excluded from scoring",
        }.get(answer or "", "Not answered")

        row = {
            "id": q.id,
            "code": q.code,
            "domain_id": q.domain_id,
            "domain_name": q.domain_name,
            "prompt": q.prompt,
            "answer": answer,
            "answer_label": answer_label,
            "points": points if applicable else None,
            "answered": answer is not None,
        }
        domain_results[q.domain_id]["questions"].append(row)
        responses.append(row)

    domains_out = []
    for domain_id in sorted(domain_results.keys(), key=lambda d: domain_results[d]["number"]):
        d = domain_results[domain_id]
        max_pts = d["max_points"]
        score = d["score"]
        pct = round((score / max_pts) * 100) if max_pts else 0
        status = _status_label(pct)
        domains_out.append(
            {
                **d,
                "compliance_pct": pct,
                "status": status,
                "service_opportunity": SERVICE_OPPORTUNITIES.get(domain_id, ""),
            }
        )

    total_score = sum(d["score"] for d in domains_out)
    total_max = sum(d["max_points"] for d in domains_out)
    overall_pct = round((total_score / total_max) * 100) if total_max else 0
    risk_level = _risk_level(overall_pct)

    critical_domains, warning_domains, _healthy_domains = _split_domains_by_status(domains_out)
    failing_domains = critical_domains + warning_domains
    critical_gaps = _build_critical_gaps(responses, question_map)
    remediation = _build_remediation(submission.company_name, failing_domains)

    return {
        "assessment_type": "technical",
        "report_title": "Compliance Gap Report",
        "survey_title": "The DPDP Act Client Gap Assessment Survey",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company_name": submission.company_name,
        "sector": submission.sector,
        "executive_overview": _executive_overview(
            submission.company_name, overall_pct, risk_level, critical_domains, warning_domains
        ),
        "summary": {
            "overall_compliance_pct": overall_pct,
            "total_score": total_score,
            "max_points": total_max,
            "risk_level": risk_level,
            "scorecard_note": _scorecard_note(overall_pct, risk_level, critical_domains, warning_domains),
            "questions_total": len(_QUESTIONS),
            "questions_answered": sum(1 for r in responses if r["answered"]),
        },
        "domains": domains_out,
        "questionnaire_responses": responses,
        "critical_gaps": critical_gaps,
        "remediation_pathway": remediation,
        "disclaimer": (
            "This technical gap assessment evaluates infrastructure and operational controls against "
            "structured DPDP compliance assessment criteria. It complements — but does not replace — "
            "legal obligation analysis or formal legal advice."
        ),
    }
