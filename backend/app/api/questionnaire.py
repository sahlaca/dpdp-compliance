from fastapi import APIRouter

from app.questionnaire.schema import QuestionnaireResponse, QuestionnaireSubmission
from app.questionnaire.questions import get_questionnaire

router = APIRouter()


@router.get("/questionnaire", response_model=QuestionnaireResponse)
def list_questions() -> QuestionnaireResponse:
    """Return the structured questionnaire for the frontend wizard."""
    return get_questionnaire()


@router.post("/questionnaire/submit")
def submit_questionnaire(submission: QuestionnaireSubmission) -> dict[str, str]:
    """
  Accept questionnaire answers.
  Full scoring + report generation wired in reports module.
  """
    return {
        "message": "Submission received. Use POST /api/v1/reports/generate to produce a gap report.",
        "submission_id": "pending",
    }
