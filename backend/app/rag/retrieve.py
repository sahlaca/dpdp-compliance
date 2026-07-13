"""Retrieve relevant legal text excerpts from the local corpus."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

from app.config import settings


@lru_cache(maxsize=1)
def _load_chunks() -> list[dict[str, Any]]:
    corpus_path = settings.corpus_dir / "chunks.json"
    if not corpus_path.is_file():
        return []
    with open(corpus_path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("chunks", [])


def _tokenize(query: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
    return [t for t in tokens if len(t) > 2]


def retrieve_citations(
    query: str,
    source_ids: list[str] | None = None,
    top_k: int = 2,
) -> list[dict[str, Any]]:
    """Simple keyword-scored retrieval over chunked legal corpus."""
    chunks = _load_chunks()
    if not chunks:
        return []

    tokens = _tokenize(query)
    if not tokens:
        return []

    scored: list[tuple[float, dict[str, Any]]] = []
    for chunk in chunks:
        if source_ids and chunk["source_id"] not in source_ids:
            continue
        text_lower = chunk["text"].lower()
        score = sum(text_lower.count(tok) for tok in tokens)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    results: list[dict[str, Any]] = []
    for score, chunk in scored[:top_k]:
        excerpt = chunk["text"]
        if len(excerpt) > 400:
            excerpt = excerpt[:397] + "..."
        results.append(
            {
                "source_id": chunk["source_id"],
                "chunk_id": chunk["id"],
                "excerpt": excerpt,
                "relevance_score": score,
                "download_url": f"/api/v1/sources/{chunk['source_id']}/download",
            }
        )
    return results


def build_search_query(act_sections: list[str], rule_references: list[str], title: str) -> str:
    parts = [title]
    for section in act_sections:
        parts.append(section.replace("Section ", "section "))
    for rule in rule_references:
        parts.append(rule.replace("Rule ", "rule "))
    return " ".join(parts)
