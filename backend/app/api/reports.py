from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.db.database import get_db
from app.db.models import SavedReport, User
from app.questionnaire.schema import QuestionnaireSubmission
from app.reports.export import (
    _report_styles,
    render_html_report,
    render_legal_report_body,
    render_pdf_report,
)
from app.reports.generator import generate_gap_report

router = APIRouter()


def _safe_filename(company_name: str, ext: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in company_name)[:40]
    return f"DPDP_Legal_Gap_Report_{safe}.{ext}"


def _persist_report(db: Session, user: User, submission: QuestionnaireSubmission, report: dict) -> None:
    db.add(
        SavedReport(
            user_id=user.id,
            company_name=submission.company_name,
            sector=submission.sector,
            assessment_type="legal",
            submission=submission.model_dump(),
            report=report,
        )
    )
    db.commit()


@router.post("/reports/generate")
def create_report(
    submission: QuestionnaireSubmission,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Score obligations and return a structured compliance gap report."""
    try:
        report = generate_gap_report(submission)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    _persist_report(db, user, submission, report)
    return report


@router.post("/reports/download")
def download_report_pdf(
    submission: QuestionnaireSubmission,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """Generate and download a professional PDF compliance report."""
    report = generate_gap_report(submission)
    _persist_report(db, user, submission, report)
    base_url = str(request.base_url).rstrip("/")

    try:
        pdf_bytes = render_pdf_report(report, base_url=base_url)
    except RuntimeError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{_safe_filename(submission.company_name, "pdf")}"',
        },
    )


@router.post("/reports/download/html")
def download_report_html(
    submission: QuestionnaireSubmission,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Generate and download an HTML version of the report (optional)."""
    report = generate_gap_report(submission)
    _persist_report(db, user, submission, report)
    base_url = str(request.base_url).rstrip("/")
    html = render_html_report(report, base_url=base_url, for_pdf=False)

    return HTMLResponse(
        content=html,
        headers={
            "Content-Disposition": f'attachment; filename="{_safe_filename(submission.company_name, "html")}"',
        },
    )


@router.post("/reports/render-html", response_class=HTMLResponse)
def render_report_html(
    report: dict[str, Any],
    user: User = Depends(get_current_user),
) -> HTMLResponse:
    assessment_type = report.get("assessment_type", "legal")
    if assessment_type != "legal":
        raise HTTPException(status_code=400, detail="Not a legal assessment report")
    fragment = (
        f"<style>{_report_styles(for_pdf=False)}</style>"
        f"{render_legal_report_body(report, base_url='', for_pdf=False)}"
    )
    return HTMLResponse(content=fragment)
