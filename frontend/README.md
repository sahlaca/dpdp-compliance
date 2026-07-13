# Frontend — DPDP Phase 1

React + Vite questionnaire wizard that calls the Python backend API.

## Run locally

```bash
npm install
npm run dev
```

App: http://localhost:5173

The dev server proxies `/api` requests to `http://localhost:8000` (start the backend first).

## Build for production

```bash
npm run build
npm run preview
```

Set `VITE_API_URL` to your deployed backend URL when not using the dev proxy.
