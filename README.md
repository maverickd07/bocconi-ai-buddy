# Bocconi AI Buddy

An "AI Buddy" for Bocconi students. Given a natural-language question, it answers with a grounded response and cites the source files it used. Built for the OpenAI × Bocconi Hackathon (May 2026).

The buddy covers 4 areas of student life:

- `relocation` — moving to Milan, housing, getting around
- `life_on_campus` — campus life, events, associations, well-being, inclusion
- `study_abroad` — exchanges, double degrees, international opportunities
- `career_readiness` — CV, job market, internships, career prospects

## How it works

- **Backend** — FastAPI service exposing `POST /ask`. RAG pipeline over ~1,600 pre-scraped Bocconi documents (~2.9M tokens). Chunks are embedded with `text-embedding-3-large`, stored in a FAISS index, retrieved per verticale, and answered with `gpt-4o-mini`. Ships with a `/health` route for Railway healthchecks.
- **Frontend** — Vite + React + TypeScript, deployed as a static site. Calls the backend via `VITE_BACKEND_URL`.
- **Knowledge base** — `backend/data/`, ~1,617 markdown files organized by verticale, each with YAML frontmatter (`verticale`, `language`, `source_url`, `title`). Full index in `backend/data/manifest.json`.

## Repository layout

```
.
├── backend/                 FastAPI + RAG service
│   ├── main.py              /ask endpoint, index loader, retrieval, generation
│   ├── data/                ~1,617 markdown docs organized by verticale + manifest.json
│   ├── Dockerfile           production image
│   ├── pyproject.toml       Python 3.13 deps (uv-managed)
│   └── railway.json         Railway deploy config
├── frontend/                Vite + React static site
│   ├── src/                 App entry
│   ├── package.json
│   └── railway.json
├── docker-compose.dev.yml   local dev environment (backend + frontend hot reload)
├── Dockerfile.backend       dev container for backend
├── Dockerfile.frontend      dev container for frontend
├── .env.example             template — copy to .env and add OPENAI_API_KEY
├── AGENTS.md                agent-facing spec (schema, constraints, embedding strategy)
├── BRIEF.md                 hackathon brief and evaluation rules
├── DESIGN.md                editorial design system for the frontend
├── DEPLOY.md                Railway two-service deploy walkthrough
└── SAMPLE_QUESTIONS.md      examples of the questions the evaluator asked
```

## Local development

Prerequisites: Docker Desktop, an OpenAI API key.

```bash
# 1. Set up your API key
cp .env.example .env
# edit .env and paste your OPENAI_API_KEY

# 2. Start dev containers
docker compose -f docker-compose.dev.yml up -d

# 3. Verify
#    Backend  → http://localhost:8000/docs
#    Frontend → http://localhost:5173

# 4. Smoke test /ask
curl -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I find housing in Milan?"}'
```

The first `/ask` call after a clean checkout will build the FAISS index from `backend/data/` (~5–10 min, one-time). Subsequent starts load the persisted index in milliseconds. The index is git-ignored — it's regenerable from the corpus.

## The `/ask` contract (frozen)

```jsonc
// Request
{ "question": "string" }

// Response
{
  "answer":    "string",
  "sources":   ["string", ...],   // paths under backend/data/
  "verticale": "relocation" | "life_on_campus" | "study_abroad" | "career_readiness"
}
```

Public, unauthenticated, single JSON body, HTTP 200 for every answer (including honest abstentions), ≤ 30 seconds. See `AGENTS.md` for the full rules.

## Deploy

Two-service Railway project: `backend/` (FastAPI) and `frontend/` (Vite static). Env vars:

- **backend** — `OPENAI_API_KEY`, optionally `FRONTEND_URL` for CORS
- **frontend** — `VITE_BACKEND_URL` (must be set **before** the frontend build; Vite inlines it)

Full walkthrough in `DEPLOY.md`.

## Credits

Built by [春。](https://github.com/) at the OpenAI × Bocconi Hackathon, May 2026. Starter, dataset, and evaluation framework by the hackathon organizers.
