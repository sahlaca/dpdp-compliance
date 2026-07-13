from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.db.database import get_db
from app.db.models import SavedReport, User
from app.technical.export import (
    render_technical_pdf_report,
    render_technical_report_body,
    technical_report_styles,
)
from app.technical.generator import generate_technical_report
from app.technical.questions import get_technical_questionnaire
from app.technical.schema import TechnicalSubmission

router = APIRouter()


def _safe_filename(company_name: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in company_name)[:40]
    return f"DPDP_Technical_Gap_Report_{safe}.pdf"


def _persist(db: Session, user: User, submission: TechnicalSubmission, report: dict) -> None:
    db.add(
        SavedReport(
            user_id=user.id,
            company_name=submission.company_name,
            sector=submission.sector,
            assessment_type="technical",
            submission=submission.model_dump(),
            report=report,
        )
    )
    db.commit()


@router.get("/technical/questionnaire")
def technical_questionnaire() -> dict:
    return get_technical_questionnaire().model_dump()


@router.post("/technical/reports/generate")
def create_technical_report(
    submission: TechnicalSubmission,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    report = generate_technical_report(submission)
    _persist(db, user, submission, report)
    return report


@router.post("/technical/reports/download")
def download_technical_report(
    submission: TechnicalSubmission,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    report = generate_technical_report(submission)
    _persist(db, user, submission, report)
    try:
        pdf_bytes = render_technical_pdf_report(report)
    except RuntimeError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{_safe_filename(submission.company_name)}"'},
    )


@router.post("/technical/reports/render-html", response_class=HTMLResponse)
def render_technical_report_html(
    report: dict[str, Any],
    user: User = Depends(get_current_user),
) -> HTMLResponse:
    if report.get("assessment_type") != "technical":
        raise HTTPException(status_code=400, detail="Not a technical assessment report")
    fragment = (
        f"<style>{technical_report_styles(for_pdf=False)}</style>"
        f"{render_technical_report_body(report)}"
    )
    return HTMLResponse(content=fragment)
