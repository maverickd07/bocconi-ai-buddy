# AGENTS.md - Bocconi Hackathon Starter

> Project context and rules for AI coding agents (Codex). Read this before any task.

## Communication style

> **Read this before answering anything.** This rule overrides the technical tone of the rest of this file. The rest of the document is written for *you* (the agent); your replies to the student must NOT sound like it.

**Who you are talking to.** A Bocconi business school student. They are smart, fluent in goals and trade-offs, and used to thinking in terms of outcomes ("the buddy answers students' questions about housing") - not in terms of stacks, schemas, or commands. Assume they do **not** know what RAG, embedding, vector store, container, endpoint, schema, or CLI mean unless they use the term first.

**Default reply shape** for any open question (e.g. "what do I need to do?", "how does this work?", "what's next?"):

1. **Start with the outcome**, in one or two plain sentences. What is the goal of this step, in the student's own world? (e.g. "We're going to make your AI buddy actually able to answer a student's question.")
2. **Then, only if needed, the concrete action**, in everyday language. Mention a command or a file only when the student is about to *do* something with it - not as a checklist of "things that exist".
3. **Stop.** Three to five sentences total is usually enough. No headed lists of 8 numbered steps unless the student explicitly asks for a step-by-step.

**Technical terms.** When a term is unavoidable, gloss it inline the first time, in 6-10 words: *"the API endpoint (the single web address the evaluator will call)"*, *"a RAG setup (we let the model read your dataset before it answers)"*. After that, use the term normally.

**Code and commands.** Show a command only when the student is about to run it now. Don't dump curl / docker / railway snippets as a reference list - that belongs in the README, not in chat. Code blocks inside source files stay technical and in English (see "Code conventions"); this section is only about what you say to the student in chat.

### Before / after - the same answer, two styles

Student asks: **"Cosa devo fare?"**

**Bad (too technical, list-heavy, no framing) - do NOT answer like this:**

> 1. Avvia l'ambiente dev: `docker compose -f docker-compose.dev.yml up -d`
> 2. Verifica backend su `http://localhost:8000/docs` e frontend su `http://localhost:5173`
> 3. Implementa `POST /ask` con schema `{question} -> {answer, sources, verticale}`
> 4. Costruisci la logica RAG sui 4 verticali ...
> 5. Deploy su Railway con due servizi (`backend/` e `frontend/`), set `VITE_BACKEND_URL` ...

This reads like a deploy runbook. The student does not yet know *why* any of this matters.

**Good (goal first, plain language, short) - answer like this:**

> Il tuo obiettivo per oggi: costruire un piccolo assistente AI che risponde alle domande di uno studente Bocconi su quattro aree della sua vita universitaria (alloggio a Milano, vita in campus, scambi all'estero, lavoro dopo la laurea).
>
> Per cominciare ti basta accendere l'ambiente di sviluppo (un comando solo, te lo lancio io) e aprire la pagina locale del backend per verificare che parta. Da li' passiamo al cuore della challenge: insegnare all'assistente a leggere i materiali ufficiali di Bocconi che trovi nella cartella `data/` e a usarli per rispondere.
>
> Vuoi che parta io con l'avvio dell'ambiente?

Notice: outcome first, no jargon, no schema dump, ends with one clear next step the student can say yes to.

## What you must build

An "AI Buddy" agent that helps Bocconi students by answering questions across 4 key areas of student life. All 4 verticals must be covered.

## The 4 verticals (all required)

1. `relocation` - moving to Milan, housing, getting around the city
2. `life_on_campus` - campus life, events, student associations, well-being, inclusion
3. `study_abroad` - exchange programs, double degrees, international opportunities
4. `career_readiness` - CV, job market, internships, career prospects

## Endpoint /ask - frozen schema (DO NOT change the signature)

The app must expose `POST /ask`:

```python
# Request
{
  "question": str    # user question (mostly English in evaluation, see "Language" below)
}

# Response
{
  "answer": str,                # natural-language answer
  "sources": list[str],         # list of file paths / identifiers used (any language)
  "verticale": str              # one of: "relocation", "life_on_campus", "study_abroad", "career_readiness"
}
```

**Critical**: the signature is frozen. The automated evaluation pipeline relies on it. Any deviation = endpoint not evaluable = `wrong` (-15) for every question.

### Scope of these rules

> **These rules apply only to `POST /ask`, the single endpoint the automated evaluator calls.** If you happen to need another route for your own frontend (the `/health` route already in the starter is the only one strictly required besides `/ask`), it is outside the scope of this contract and is not bound by the constraints below. Conversely, the constraints cannot be relaxed by moving logic somewhere else - the evaluator only sees `/ask`. Default to keeping the surface area minimal: the challenge is won on the quality of `/ask`, not on extra routes.

### Hard constraints on `/ask` (non-negotiable)

The evaluator does **one** `POST` request and reads **one** JSON response. If your endpoint deviates on any of the points below, every question scores `wrong` (-15) -> floor of -1200 on Level 1.

- **Path**: exactly `/ask` at the root of your backend public URL. Not `/api/ask`, not `/v1/ask`, not `/buddy/ask`.
- **Method**: `POST` (only). No `GET /ask?question=...`.
- **Request body**: a single JSON object `{"question": "<string>"}`. No extra required fields. No required headers beyond `Content-Type: application/json`.
- **Auth**: `/ask` must be **publicly callable with no authentication**. No Bearer token, no API key header, no IP allowlist, no Cloudflare/Railway "private network", no Basic Auth.
- **Response status**: HTTP `200` for any answer (including "I don't know"). Do not return `4xx`/`5xx` to signal "no info" - return `200` with an honest abstention in the `answer` field.
- **Response body**: a single JSON object with **exactly** the keys `answer` (string), `sources` (list of strings), `verticale` (one of the 4 fixed values). Extra keys are ignored, but the three required keys must be present and well-typed.
- **No streaming**. The response body must be a complete JSON object delivered as a single body. Do **NOT** use Server-Sent Events (`text/event-stream`), do **NOT** use NDJSON (one JSON per line), do **NOT** use the OpenAI SDK with `stream=True` and forward chunks. The evaluator calls `response.json()` once on the full body - if it cannot parse it, the question scores `wrong`.
- **No async/job pattern**. Do not return `{"job_id": "..."}` and require a second call to `/ask/result/{id}`. The answer must be in the body of the first response.
- **Latency**: full response within 30 seconds. See "Latency constraint" below.

If Codex (or you) is tempted to "improve" any of the above for security, performance, or elegance: don't. The contract is locked because the evaluator is locked - any deviation is a regression, not an improvement.

## Latency constraint

The `/ask` endpoint must respond **within 30 seconds** for every question.

Responses over 30s are truncated by the evaluation pipeline = `wrong` (-15) for that question (system errors count as wrong answers). Balance "sophisticated agent" with "agent that responds in time". If you build a multi-step agent with many tool calls, consider caching or fewer steps.

## When the LLM call errors out

OpenAI calls can fail in a 6-hour event for three reasons:

1. **Rate limit** (HTTP 429): too many tokens-per-minute, common on smaller / older snapshots that have tighter per-org limits.
2. **Transient network error** (5xx, socket timeout): more common on cold starts.
3. **Quota exhausted**: the redemption code's $50 ran out (rare in 6 hours, but possible if you re-embed the corpus 50 times - see "Embedding strategy" below).

**Default behavior**: retry with exponential backoff, then fall back gracefully.

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((RateLimitError, APIError)),
)
def call_llm(messages, model):
    return client.chat.completions.create(model=model, messages=messages, timeout=20)
```

If retries still fail, return HTTP `200` with `answer: "I cannot answer right now."` rather than a 5xx. From the evaluator's point of view, an honest abstention scores `0` (no_answer) while a 5xx scores `-15` (wrong). A graceful fallback is a 15-point swing per failing question.

For **persistent rate limits**: your first move is to **switch model family** (web-search the current OpenAI lineup, see "Latest LLM models" below), not "raise the retry count". Older snapshots throttle harder than newer ones.

## Knowledge base paths

> **Snapshot date: 2026-05-02.** The dataset is a snapshot at this date. The
> 80 hidden evaluation questions reflect what was current in May 2026 - the
> running 2025-26 academic year and the open application cycle for 2026-27.

Pre-cleaned data is provided inside the backend container under `backend/data/` (mounted at `/app/data` at runtime), **already organized by verticale**:

- `backend/data/relocation/` (~119 files, ~236k tokens)
- `backend/data/life_on_campus/` (~473 files, ~508k tokens)
- `backend/data/study_abroad/` (~132 files, ~349k tokens) - includes 18 Farnesina country advisories (viaggiaresicuri.it)
- `backend/data/career_readiness/` (~893 files, ~1.79M tokens) - includes 2 AlmaLaurea national synthesis reports
- `backend/data/manifest.json` - full index of all files with metadata
- `backend/data/extra-sources.md` - curated list of additional public sources (some bundled, some pointers only)
- `backend/data/README.md` - dataset documentation

**Total: ~1,617 files, ~2.88M tokens**, scraped from `unibocconi.it`, `sdabocconi.it`, `bocconialumni.it`, `traileoni.it`, *.unibocconi.eu departments and labs, plus selected Comune di Milano open data, housing partners, student-life guides, Farnesina country advisories (viaggiaresicuri.it) and AlmaLaurea graduate surveys. PDFs (academic calendar, fees, factsheets, exchange brochures, campus map, AlmaLaurea reports) processed via Mistral OCR or text extraction.

Every file has YAML frontmatter with `verticale`, `language`, `source_url`, `title`, `token_estimate`. Use the `verticale` field for metadata filtering at query time.

Use these files as the RAG knowledge base. You cannot fetch external data at runtime, but `extra-sources.md` lists additional URLs you could pre-download into the image if you want to differentiate.

## Stack available in the container

Pre-installed (dev environment):

- **Python 3.13**: FastAPI, Uvicorn, Pydantic, OpenAI SDK
- **Node 22**: Vite, React, TypeScript

Suggested but **not pre-installed** (uncomment in `backend/pyproject.toml` and run `uv sync` if you want them):

- RAG framework: `llama-index`, `langchain`, `langchain-openai`
- Vector store: `faiss-cpu`, `chromadb`, `sqlite-vec`
- Postgres + pgvector: `psycopg`, `pgvector`, `sqlalchemy`

You can swap any piece (Svelte instead of React, Flask instead of FastAPI) **as long as `/ask` matches the schema** and the app builds via the provided `Dockerfile.prod`.

## Latest LLM models: do NOT trust your training data

Your training cutoff is older than the event date. The OpenAI model lineup you remember (e.g. `gpt-4`, `gpt-4-turbo`, `gpt-4.1`) may be deprecated, throttled, or simply not the smartest available option in May 2026.

**Before you hardcode a model name, web-search OpenAI's current model list** (e.g. `platform.openai.com/docs/models` or a fresh `https://openrouter.ai/models` query). The student's $50 of OpenAI credit is best spent on a *current* model that fits the 30s latency budget, not on a legacy snapshot with hard rate limits.

Heuristic for picking:

- **Answer generation**: a current "small / fast" general model (sub-$1 per million input tokens, sub-2s typical latency, multilingual).
- **Re-ranking** or query rewriting: an even smaller model. Latency adds up across many calls.
- **Embeddings**: at the time of writing, `text-embedding-3-large` is still strong for multilingual retrieval. If a successor exists at the event date, prefer it.

If the student tells you their preferred model is rate-limiting (HTTP 429 / "tokens per minute exceeded"), **switch to a sibling model in the same family rather than wait**. Re-deploying takes seconds. Combine with the retry pattern in "When the LLM call errors out".

## Vector store - 3 patterns to choose from

- **FAISS in-memory**: simplest, `.faiss` file in `data/`, loaded into RAM at startup
- **Chroma file-based**: local persistence, no external service
- **SQLite + sqlite-vec**: embedded vector DB, native SQL filtering by verticale (recommended for production-like pattern: `WHERE verticale = 'career_readiness' ORDER BY embedding <-> $1`)

Pick one. All three work in a single container.

## Embedding strategy: prebuild once, persist, never reindex at runtime

The dataset is ~2.88M tokens / ~6,000 chunks. Embedding it costs roughly $0.40 with `text-embedding-3-large` and takes 5-10 minutes wall-clock. **You do this once, locally, BEFORE deploying.** You do NOT do it inside the running container.

The pattern:

1. Write a one-shot script (e.g. `backend/scripts/build_index.py`) that walks `data/`, chunks each markdown file, embeds the chunks, and saves the index to `backend/data/index/` (FAISS file, Chroma collection, or sqlite-vec table).
2. Run it locally: `uv run python backend/scripts/build_index.py`. Verify the index file exists and is non-empty.
3. The Dockerfile already `COPY`s `backend/` (including `data/`) into the image, so the prebuilt index ships with the deploy.
4. At app startup, FastAPI loads the index from disk in milliseconds. **No embedding calls at startup. No embedding calls at request time** beyond the user's own question (one tiny call).

**Anti-patterns to avoid:**

- *"I'll embed at first request."* The first user waits 8 minutes, the platform times out, every question scores `wrong` while the index builds.
- *"I'll embed at app startup."* The Railway healthcheck times out, the deploy fails, or every cold start costs minutes of downtime.
- *"I'll re-embed on every deploy."* You're paying $0.40 + 8 minutes for nothing every time you change a UI label.

If the student wants to add a new source mid-event (extra Numbeo file, ISTAT JSON, etc.): prebuild a delta index locally and ship the merged file. The runtime never embeds the corpus.

The index file is allowed in `.gitignore` (it is regenerable), but it must NOT be in `.dockerignore` - the production image needs it.

## Environment variables

The organizers give you a **redemption code**, not a ready-made API key. You redeem it on [platform.openai.com](https://platform.openai.com) (Settings -> Billing -> Credit grants) to load $50 of credit on your account, then you create your own API key from the dashboard (`Create new secret key`). That generated key goes in `.env`:

```
OPENAI_API_KEY=sk-...
```

**Never commit `.env`** (already in `.gitignore`). **Never hardcode the key** in source files. **Never paste the redemption code itself** anywhere - it's a one-shot, redeem and discard.

## Language

- **Evaluation questions are mostly in English.** Make sure your agent handles English well.
- **Knowledge base is mixed Italian + English** (Bocconi reality - admin/services often IT, international programs EN). Don't translate it; embed as-is.
- A multilingual embedding model is **strongly recommended** for cross-lingual retrieval (e.g., `text-embedding-3-large`). An EN question may need to retrieve IT docs.
- **Nice-to-have**: detect the question language and reply in the same language. Not strictly enforced, but Italian-speaking users in the audience will appreciate it.
- Bocconi-specific terms (CLEF, Triennale, Magistrale, Borse Merit, etc.) often have no clean translation - keep the original term, optionally glossed.

## Code conventions

- Code, identifiers, comments, file names, this repo's documentation: **English (always)**
- AI Buddy responses to users: free choice (English is fine; matching the question language is a plus)

## What is NOT provided (you build it)

- The RAG pipeline (chunking, embedding, retrieval, generation)
- Routing logic to detect the verticale
- The frontend UI (placeholder only - `<div>Build me</div>`)
- System prompts
- Frontend ↔ backend integration
- Tests (optional)

## What IS already set up

- Docker dev environment (backend + frontend, hot reload via volume mount)
- `POST /ask` route with frozen schema (returns 501 Not Implemented until you implement it)
- **Two-service Railway deploy**: `backend/Dockerfile` + `backend/railway.json` for the API, `frontend/railway.json` for the static site. Each service is simple and builds independently.
- Pre-cleaned dataset of ~1,617 files in `data/` organized by verticale
- `.env.example` template
- All essential dependencies installed in the container

## Workflow

1. Ask me (Codex) to **start the dev environment**. I'll run `docker compose -f docker-compose.dev.yml up -d`.
2. Verify backend at http://localhost:8000/docs and frontend at http://localhost:5173
3. Implement the `/ask` endpoint (see kickoff prompt in `README.md`)
4. Iterate: add UI, refine prompts, expand knowledge base coverage
5. **Deploy to Railway** early - see `DEPLOY.md`. There is a ready-made prompt you can paste to make me handle the full deploy.

## Build / run commands (you can also ask me to run them)

| Command | What it does |
| --- | --- |
| `docker compose -f docker-compose.dev.yml up -d` | Start backend + frontend dev containers |
| `docker compose -f docker-compose.dev.yml logs -f` | Stream logs |
| `docker compose -f docker-compose.dev.yml down` | Stop containers |
| `curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"test"}'` | Smoke test the endpoint |
| `cd backend && railway up` | Deploy backend service (after `railway login` + `railway init`) |
| `cd frontend && railway up` | Deploy frontend service (in the same project) |

## Deployment requirement (important)

The automated evaluator hits the **backend's public URL** at `POST /ask` with ~80 questions. Deploy is two services on the same Railway project:

- `backend/` → Python FastAPI service. Public URL = the one the evaluator submits to.
- `frontend/` → Vite static site. Calls the backend via `VITE_BACKEND_URL`.

Set env vars on Railway (NEVER commit `.env`):
- On **backend** service: `OPENAI_API_KEY=sk-...` (and optionally `FRONTEND_URL=...` to lock down CORS)
- On **frontend** service: `VITE_BACKEND_URL=https://<backend-public-url>` (must be set BEFORE the build - Vite inlines it)

Verify with `curl https://<backend-url>/health` returning `{"status":"ok"}`. Full step-by-step in `DEPLOY.md`.

## Best practices (specific to this challenge)

- Start by getting **one verticale working end-to-end** (e.g., `career_readiness`), then extend to the others (they are variations of the same pattern, only the data domain changes)
- Treat the 30s timeout as a design constraint from day 1, not an optimization step
- `sources` in the response are checked for grounding - return real file paths from `data/`, not made-up references
- The evaluator asks mostly in English - make sure English works well; Italian handling is a plus, not a requirement
- Keep system prompts concise to reduce latency

## Going beyond MVP

The student has 6 hours. A working RAG over the 4 verticali is the **baseline**, not the finish line. Level 2 of the evaluation (`BRIEF.md`, section 7) explicitly rewards differentiation, polish, extra data sources, creativity. Top-15 projects are the ones that go beyond.

**Your job, after the baseline answers all 4 verticali correctly**: proactively propose ONE concrete upgrade to the student. Don't ask a vague "what next?" - pick a specific upgrade, frame the *outcome* in plain language ("this would make the buddy noticeably better at comparative questions like 'which partner has the most exchanges'"), tag the difficulty, and offer to implement it. If the student says no, propose another. If they say yes, do it - then propose the next one when done.

Pick from the menu below. Each entry is `<upgrade> | <difficulty> | <when it pays off>`.

**Retrieval quality**

- Hybrid retrieval (BM25 + dense) | medium | catches keyword-exact matches the embeddings miss (program codes, association acronyms, course IDs).
- Re-ranking with a small LLM call | easy | bumps the most relevant chunks to the top of context, often turns a `partial` answer into `correct`.
- Query rewriting / decomposition | medium | helps comparative questions ("which partner university has the most exchanges in finance?") and multi-fact questions.
- Per-verticale system prompts | easy | a tuned prompt per verticale beats a generic one.

**Coverage**

- Pull 1-2 sources from `data/extra-sources.md` (ISTAT, Numbeo, Comune di Milano open data, ranking JSONs) and bake them into the image.
- Add a deterministic small lookup (e.g. ATM ticket prices, university partner counts) for high-traffic facts the LLM gets wrong.

**UX (see `DESIGN.md` for the editorial spec)**

- 4-card landing page that pre-fills the chat with a verticale-specific question.
- Streamed "thinking" UI text while the model runs (intermediate reasoning shown to the user, final answer still single-shot - the `/ask` schema is frozen).
- Source citations as clickable chips that open the original file.
- Conversation memory across turns (small in-memory ring buffer of the last 3-4 turns).

**Infra (only if it adds visible value, not for its own sake)**

- Postgres on Railway for conversation logs + a tiny analytics view ("most asked verticale today").
- Caching of identical questions in SQLite (sub-second response on repeats, dodges the 30s budget).

**Important**: do NOT over-engineer. Each upgrade has to make a *visible* difference to the answer the evaluator sees, OR to the UI a human judge sees. "Refactor the code into 7 modules" is not an upgrade.

### Pacing the 6 hours

A reasonable rhythm:

- **Hours 0-1**: docker up, `/ask` returns a real (even if mediocre) answer for ONE verticale.
- **Hours 1-2**: extend to all 4 verticali. First Railway deploy (even if rough).
- **Hours 2-3**: persist the embedding index (see "Embedding strategy"). Wire the frontend to `/ask`. Polish the UI per `DESIGN.md`.
- **Hours 3-5**: 2-3 upgrades from the menu above. Re-deploy after each.
- **Hour 5-6**: smoke-test the deployed URL with sample questions, write the 200-word product description, submit.

Push back politely if the student wants to start with infra fancy-stuff before the baseline works. The order matters.
