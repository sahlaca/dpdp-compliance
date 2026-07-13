#!/usr/bin/env python3
"""Extract text from source PDFs, chunk, and build searchable corpus."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Allow running as: python scripts/ingest_corpus.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pypdf import PdfReader  # noqa: E402

from app.config import settings  # noqa: E402
from app.sources.catalog import load_manifest  # noqa: E402


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"[Page {i}]\n{text}")
    return "\n\n".join(pages)


def chunk_text(text: str, source_id: str, chunk_size: int = 1000, overlap: int = 150) -> list[dict]:
    text = re.sub(r"\s+", " ", text).strip()
    chunks: list[dict] = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        snippet = text[start:end].strip()
        if len(snippet) > 80:
            chunks.append(
                {
                    "id": f"{source_id}_{idx}",
                    "source_id": source_id,
                    "text": snippet,
                    "start_char": start,
                }
            )
            idx += 1
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def main() -> None:
    manifest = load_manifest()
    all_chunks: list[dict] = []
    stats: dict[str, int] = {}

    for item in manifest["sources"]:
        pdf_path = settings.sources_dir / item["filename"]
        if not pdf_path.is_file():
            print(f"SKIP (missing): {item['id']}")
            continue
        print(f"Ingesting: {item['id']} ({item['filename']})")
        text = extract_text(pdf_path)
        chunks = chunk_text(text, item["id"])
        all_chunks.extend(chunks)
        stats[item["id"]] = len(chunks)
        print(f"  -> {len(chunks)} chunks, {len(text):,} chars")

    settings.corpus_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = settings.corpus_dir / "chunks.json"
    with open(corpus_path, "w", encoding="utf-8") as f:
        json.dump({"chunk_count": len(all_chunks), "stats": stats, "chunks": all_chunks}, f, indent=2)

    print(f"\nWrote {len(all_chunks)} chunks to {corpus_path}")


if __name__ == "__main__":
    main()
