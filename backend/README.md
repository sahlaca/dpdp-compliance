# Backend — DPDP Phase 1

Python FastAPI service for questionnaire intake, deterministic obligation scoring, and gap report generation.

## Layout

```
app/
├── api/            # HTTP routes
├── questionnaire/  # Question definitions + Pydantic schemas
├── rules/          # Obligation scoring engine (deterministic)
├── rag/            # Legal corpus ingest + retrieval
├── reports/        # Gap report assembly
├── config.py
└── main.py
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Key endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/questionnaire` | Questionnaire schema for frontend |
| GET | `/api/v1/sources` | List legal sources with download links |
| GET | `/api/v1/sources/{id}/download` | Download a source PDF for verification |
| POST | `/api/v1/reports/generate` | Generate gap report from answers |

## Legal data

Source PDFs live in `../data/sources/`. Re-download or rebuild:

```bash
python scripts/download_sources.py   # fetch PDFs from official URLs
python scripts/ingest_corpus.py    # rebuild searchable text corpus
```
