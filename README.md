# DPDP Phase 1 — Compliance Guidance Generator

Questionnaire-driven app that produces personalized DPDP compliance gap reports for organizations subject to India's DPDP Act 2023 and Rules 2025.

**Full documentation:** [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)

## Structure

```
dpdp-phase1/
├── backend/     # Python FastAPI API, rules engine, RAG, report generation
├── frontend/    # React + Vite web UI (questionnaire wizard + report view)
└── docs/        # Planning and specification documents
```

## Quick start

### Docker (recommended for demos / sharing)

```bash
docker compose up --build
```

Open **http://localhost:8888** — see [DOCKER.md](./DOCKER.md) for full instructions.

### Local development

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Phase 1 scope

- Structured questionnaire about data practices (33 questions, 39 obligations)
- Deterministic obligation scoring (met / partial / not met)
- Legal corpus built from downloaded DPDP Act + Rules PDFs
- Per-obligation citations with downloadable source PDFs for instant verification
- Prioritized action plan (Nov 2026 / May 2027 deadlines)

**Out of scope for v1:** consent management, document drafting, system integrations.

## Disclaimer

Outputs are compliance guidance, not legal advice.
