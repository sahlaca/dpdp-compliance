# Running with Docker (CEO / presentation)

One command starts the full app. Your CEO opens **one URL** in the browser.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed (Mac or Windows)

## Start the app

```bash
cd dpdp-phase1
cp .env.example .env
# Generate secrets (run each command and paste into .env):
#   openssl rand -hex 32   → JWT_SECRET
#   openssl rand -hex 24   → POSTGRES_PASSWORD
docker compose up --build
```

PostgreSQL data persists in the `postgres_data` Docker volume across restarts.

Wait until you see the backend health check pass, then open:

**http://localhost:8888**

## Stop the app

```bash
docker compose down
```

## Architecture

```
Browser → http://localhost:8888
              ↓
         nginx (frontend container)
              ├── /        → React app (static files)
              └── /api/*   → FastAPI backend
```

**Why nginx?** Single entry point for presentations — no separate frontend/backend ports. nginx serves the UI and proxies API calls to the backend.

## Sharing with your CEO

**Option A — Share the project folder**

1. Zip the `dpdp-phase1` folder (include `data/sources/` PDFs)
2. CEO installs Docker Desktop
3. CEO runs `docker compose up --build`
4. Opens http://localhost:8888

**Option B — You host it**

Deploy the same `docker compose` to a small cloud VM (DigitalOcean, AWS, etc.) and share the public URL.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8888 in use | Change `8888:80` to another host port (e.g. `9090:80`) in `docker-compose.yml` |
| PDFs missing | Ensure `data/sources/*.pdf` exist; run `python backend/scripts/download_sources.py` |
| Build slow first time | Normal — subsequent starts are faster |
| `data/corpus/chunks.json` missing | Run `python backend/scripts/ingest_corpus.py` before dockerizing |
| PDF download fails | Rebuild backend: `docker compose up --build` (requires WeasyPrint in image) |

## Rebuild after code changes

```bash
docker compose up --build
```
