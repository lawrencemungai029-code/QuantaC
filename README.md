# Quanta Crescent — Opportunity Board MVP

## Overview
A full-stack opportunity board for hackathons, internships, and more. Built with FastAPI, React, Tailwind, and ASI1 AI integration. See full requirements in the project spec.

## Quick Start (Local Dev)

### Backend
1. Copy `.env.example` to `.env` and fill in your ASI1 and DB credentials.
2. Install Python 3.10+ and run:
   ```sh
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend
1. In a new terminal:
   ```sh
   cd frontend
   npm install
   npm run dev
   ```

### Seed Data
- On first run, call `POST /api/v1/seed` to load demo data.

## Deployment

### Frontend (Render)
- Connect GitHub repo to Render.
- Root: `/frontend`
- Build: `npm install && npm run build`
- Start: `serve -s build`
- Set env: `REACT_APP_API_BASE_URL` to backend public URL.

### Backend (Codespaces/Render)
- For dev: `uvicorn backend.app.main:app --reload --port 8000`
- For prod: deploy to Render/Heroku/Railway. (Add Procfile if needed.)

### GitHub Actions
- Add `GITHUB_TOKEN` and `ASI_API_KEY` to repo secrets.
- Orchestrator runs every 6 hours via `.github/workflows/ai_orchestrator.yml`.

## Credentials Needed
- ASI1 credentials: `ASI_ENDPOINT`, `ASI_API_KEY` (required for AI integration)
- GitHub repo connection (for Render deploy and GitHub Actions)

## Example: Call AI Endpoint
```sh
curl -X POST http://localhost:8000/api/v1/ai/update_opportunities \
  -H "Authorization: Bearer <INTERNAL_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '[{"title": "Sample Hackathon", "organization": "Devpost", ...}]'
```

## See full instructions and requirements in the project spec.
