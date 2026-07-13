from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.auth.security import create_access_token, hash_password, verify_password
from app.db.database import get_db
from app.db.models import LoginEvent, SavedReport, User

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    company_name: str | None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ReportHistoryItem(BaseModel):
    id: int
    company_name: str
    sector: str
    assessment_type: str
    generated_at: str
    summary: dict


def _user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        company_name=user.company_name,
    )


def _record_login(db: Session, user: User, request: Request) -> None:
    user.last_login_at = datetime.now(timezone.utc)
    db.add(
        LoginEvent(
            user_id=user.id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    )
    db.commit()


@router.post("/register", response_model=AuthResponse)
def register(body: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> AuthResponse:
    if db.query(User).filter(User.email == body.email.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=body.email.lower(),
        full_name=body.full_name.strip(),
        company_name=body.company_name.strip() if body.company_name else None,
        password_hash=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _record_login(db, user, request)
    token = create_access_token(user.id, user.email)
    return AuthResponse(access_token=token, user=_user_out(user))


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    _record_login(db, user, request)
    token = create_access_token(user.id, user.email)
    return AuthResponse(access_token=token, user=_user_out(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return _user_out(user)


@router.get("/reports", response_model=list[ReportHistoryItem])
def report_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ReportHistoryItem]:
    rows = (
        db.query(SavedReport)
        .filter(SavedReport.user_id == user.id)
        .order_by(SavedReport.generated_at.desc())
        .limit(50)
        .all()
    )
    return [
        ReportHistoryItem(
            id=r.id,
            company_name=r.company_name,
            sector=r.sector,
            assessment_type=getattr(r, "assessment_type", None) or r.report.get("assessment_type", "legal"),
            generated_at=r.generated_at.isoformat(),
            summary=r.report.get("summary", {}),
        )
        for r in rows
    ]


@router.get("/reports/{report_id}")
def get_saved_report(
    report_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    row = db.query(SavedReport).filter(SavedReport.id == report_id, SavedReport.user_id == user.id).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return row.report
