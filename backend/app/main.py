from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, health, questionnaire, reports, sources, technical
from app.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="DPDP Compliance Guidance API",
    description="Structured DPDP compliance assessment: questionnaire intake, obligation scoring, and gap report generation.",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(questionnaire.router, prefix="/api/v1", tags=["questionnaire"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(sources.router, prefix="/api/v1", tags=["sources"])
app.include_router(technical.router, prefix="/api/v1", tags=["technical"])
