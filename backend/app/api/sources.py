from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.sources.catalog import get_catalog, get_source_by_id, get_source_file_path

router = APIRouter()


@router.get("/sources")
def list_sources() -> dict:
    """List all legal source documents with download links for verification."""
    catalog = get_catalog()
    return catalog.model_dump()


@router.get("/sources/{source_id}")
def get_source(source_id: str) -> dict:
    source = get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source.model_dump()


@router.get("/sources/{source_id}/download")
def download_source(source_id: str) -> FileResponse:
    """Download a stored source PDF so users can verify citations instantly."""
    source = get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    file_path = get_source_file_path(source_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Source file not available locally")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=source.filename,
        headers={"Content-Disposition": f'attachment; filename="{source.filename}"'},
    )
