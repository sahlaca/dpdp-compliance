from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from app.config import settings


class SourceDocument(BaseModel):
    id: str
    title: str
    type: str
    filename: str
    official_url: str
    publisher: str
    description: str
    effective_date: str
    gazette_reference: Optional[str] = None
    download_url: Optional[str] = None
    file_available: bool = False
    file_size_bytes: Optional[int] = None


class ImplementationPhase(BaseModel):
    phase: str
    effective_date: str
    description: str


class SourcesCatalog(BaseModel):
    version: str
    last_updated: str
    sources: list[SourceDocument]
    implementation_phases: list[ImplementationPhase]


def _manifest_path() -> Path:
    return settings.sources_dir / "manifest.json"


def load_manifest() -> dict:
    with open(_manifest_path(), encoding="utf-8") as f:
        return json.load(f)


def get_catalog() -> SourcesCatalog:
    data = load_manifest()
    sources: list[SourceDocument] = []
    for item in data["sources"]:
        file_path = settings.sources_dir / item["filename"]
        file_available = file_path.is_file()
        sources.append(
            SourceDocument(
                **item,
                download_url=f"/api/v1/sources/{item['id']}/download" if file_available else None,
                file_available=file_available,
                file_size_bytes=file_path.stat().st_size if file_available else None,
            )
        )
    return SourcesCatalog(
        version=data["version"],
        last_updated=data["last_updated"],
        sources=sources,
        implementation_phases=[ImplementationPhase(**p) for p in data["implementation_phases"]],
    )


def get_source_file_path(source_id: str) -> Optional[Path]:
    data = load_manifest()
    for item in data["sources"]:
        if item["id"] == source_id:
            path = settings.sources_dir / item["filename"]
            return path if path.is_file() else None
    return None


def get_source_by_id(source_id: str) -> Optional[SourceDocument]:
    catalog = get_catalog()
    return next((s for s in catalog.sources if s.id == source_id), None)

