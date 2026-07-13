from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _migrate_saved_reports_assessment_type()


def _migrate_saved_reports_assessment_type() -> None:
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "saved_reports" not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns("saved_reports")}
    if "assessment_type" not in cols:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE saved_reports "
                    "ADD COLUMN assessment_type VARCHAR(32) NOT NULL DEFAULT 'legal'"
                )
            )
