"""Build human-readable questionnaire response summary for reports."""

from __future__ import annotations

from typing import Any

from app.questionnaire.questions import get_questionnaire
from app.questionnaire.schema import Question, QuestionType


def _label_for_value(question: Question, value: str) -> str:
    if not question.options:
        return value
    for opt in question.options:
        if opt.value == value:
            return opt.label
    return value


def _format_answer(question: Question, raw: Any) -> str:
    if question.type == QuestionType.BOOLEAN:
        return "Yes" if raw is True else "No"
    if question.type == QuestionType.SINGLE_CHOICE:
        return _label_for_value(question, str(raw))
    if question.type == QuestionType.MULTI_CHOICE:
        if not isinstance(raw, list) or not raw:
            return "None selected"
        return ", ".join(_label_for_value(question, str(v)) for v in raw)
    if question.type == QuestionType.NUMBER:
        return str(raw)
    return str(raw)


def build_questionnaire_responses(answers: dict[str, Any]) -> list[dict[str, Any]]:
    questionnaire = get_questionnaire()
    rows: list[dict[str, Any]] = []
    for question in questionnaire.questions:
        answered = question.id in answers
        rows.append(
            {
                "id": question.id,
                "section": question.section,
                "prompt": question.prompt,
                "answered": answered,
                "answer_display": _format_answer(question, answers[question.id]) if answered else "Not answered",
            }
        )
    return rows
