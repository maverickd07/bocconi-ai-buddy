# Deploy guide - Railway (two services)

> Step-by-step guide to deploy your AI Buddy to Railway. **You can ask Codex to do all of this for you** - paste the prompt at the bottom of this file into the Codex chat.
> A Yellow Tech mentor team will be in the room throughout the event for any deploy issues.
> **Don't leave the deploy for the last hour.** Plan your first deploy around hour 3 of the event, even if `/ask` still returns 501.

## No GitHub needed

This deploy is **fully direct from your local machine via the Railway CLI**. You do **not** need a GitHub account, a Git remote, or to push your code anywhere public. The `railway up` command uploads your local folder straight to Railway, which builds and deploys it.

The only accounts required:
- A free Railway account (sign up with email)
- The OpenAI redemption code the organizers give you on the day, redeemed on your OpenAI account so you can generate your own API key

That's it. Your code stays on your laptop and on Railway.

## Architecture

You deploy **two services** to Railway, both inside the same project:

```
Railway project: bocconi-buddy-yourname
├── backend service   →  Python FastAPI    →  https://bocconi-buddy-backend-yourname.up.railway.app
└── frontend service  →  Vite static site  →  https://bocconi-buddy-frontend-yourname.up.railway.app
```

The **automated evaluator hits the backend URL** at `/ask` (this is the URL you submit). The frontend is what users see; it calls the backend via the env var `VITE_BACKEND_URL`.

Why two services and not one container?
- Simpler builds (Python only / Node only - no fragile multi-stage)
- Independent deploys (change frontend without rebuilding backend)
- Standard production pattern

## Prerequisites

1. **Railway account** (free tier): https://railway.com
2. **Railway CLI** installed:
   ```bash
   npm install -g @railway/cli
   # or: brew install railway
   ```
3. **Working local build** - test first that `docker compose -f docker-compose.dev.yml up` works.

## Pick your deployment region (EU recommended)

Railway has 4 regions: US West, US East, EU West (Amsterdam, `europe-west4`), Southeast Asia (Singapore). The default depends on your account setting. **For a Bocconi event, the right answer is EU West Metal (Amsterdam)**: the evaluator and the room sit in Europe, so EU = lower latency, lower jitter, fewer 30-second timeouts.

Set it ONCE before running `railway init`:

1. Open [railway.com](https://railway.com) -> click your avatar -> **Account Settings** -> **Default Region** -> select **EU West Metal (Amsterdam)**.
2. From now on every new service you create defaults to EU.

If you forgot and your service is already in US, you can move it post-deploy from the CLI:

```bash
railway scale --service <service-name> --europe-west4=1
```

This redeploys the service in the EU region. Verify with `railway status`.

> Note: `railway.json` does NOT support a `region` key for single-replica services - region is an account / service-level setting only, not config-as-code.

## Step-by-step: deploy the backend

### 1. Login

```bash
railway login
```

### 2. Initialize a Railway project

```bash
cd starter/backend/
railway init
```

Pick "Empty Project" and give it a name (e.g. `bocconi-buddy-yourname`). The first service in this project will be the backend.

### 3. Deploy the backend

```bash
railway up
```

Railway reads `backend/railway.json`, builds with `backend/Dockerfile` (which copies the backend code + the bundled `data/` knowledge base into the image), and deploys.

> **Heads up - service naming**: the first service in a new Railway project inherits the project name. So if your project is `bocconi-buddy-mario`, the backend service is also called `bocconi-buddy-mario` by default. Optionally rename it to something like `backend` or `api` from the Railway dashboard - cleaner for the dashboard, but cosmetic for the rest.

> **Domain pattern**: Railway generates domains like `<service-name>-<env>-<random>.up.railway.app`. The `-random` suffix appears when the service name clashes with another tenant's service (very common for generic names like `frontend` / `backend`). To get a clean domain like `bocconi-buddy-mario-production.up.railway.app`, **use a unique service name** (your full project name + `-api` or `-web` works well). Example:
>
> - `bocconi-buddy-mario-api` → `bocconi-buddy-mario-api-production.up.railway.app` (clean)
> - `backend` → `backend-production-79c1.up.railway.app` (random suffix added)
>
> The eval pipeline doesn't care about the URL aesthetics - it accepts any. Pick what's easiest.

> **`--detach` warning**: if you use `railway up --detach` (background mode), the CLI loses its link to the service. Re-link with `railway service <project-name>`. With plain `railway up` (foreground, shows live build logs) the link is preserved.

### 4. Set the OpenAI API key on the backend service

Use the `sk-...` key you generated **after redeeming your code** on platform.openai.com. The redemption code itself never leaves your OpenAI account.

```bash
railway variables --set OPENAI_API_KEY=sk-your-real-key
```
Or open the Railway dashboard → backend service → Variables → New Variable. **Never commit the key**.

### 5. Generate a public URL for the backend

```bash
railway domain
```

You get something like `bocconi-buddy-backend-yourname.up.railway.app`. **Copy it - the evaluator submits to this URL.**

### 6. Smoke test the backend

```bash
curl https://<backend-url>/health
# Expected: {"status":"ok"}

curl -X POST https://<backend-url>/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"test"}'
# 501 until you implement /ask
```

## Step-by-step: deploy the frontend

### 7. Add a second service for the frontend

From the dashboard: project → "+ New" → "Empty Service" → name it (e.g. `<your-project>-web`).

Or from CLI, in a new terminal:
```bash
cd starter/frontend/
railway link                              # link to the existing project
railway add --service <your-project>-web  # create a new service with a unique name
railway service <your-project>-web        # link CLI to it
railway up                                # deploy this folder
```

> **Tip on service names**: pick something **unique to you** to avoid Railway adding a random suffix to your domain. `frontend` is too common and you'll likely get `frontend-production-79c1.up.railway.app`. `bocconi-buddy-mario-web` will get `bocconi-buddy-mario-web-production.up.railway.app` - cleaner.

Railway reads `frontend/railway.json`, runs `npm install && npm run build`, and serves with `vite preview`.

### 8. Set `VITE_BACKEND_URL` on the frontend service

```bash
railway variables --set VITE_BACKEND_URL=https://<backend-url>
```
Use the URL from step 5. **This must be set before building** - Vite inlines it at build time.

### 9. Generate a public URL for the frontend

```bash
railway domain
```

### 10. (Optional) Lock down CORS on the backend

For tighter security, set `FRONTEND_URL` on the **backend** service to the frontend's public URL:
```bash
# Switch to backend service first
railway service backend
railway variables --set FRONTEND_URL=https://<frontend-url>
```

Without this, the backend allows any origin (`*`) - fine for the hackathon, looser than production.

## Submission

Submit the **backend URL** (not the frontend) to the hackathon form. That is what the evaluator hits.

Optionally also submit the frontend URL for the human-evaluation pass (Level 2).

## Test your deploy mid-event

The first time you deploy, things can go wrong (env vars, build errors, healthcheck timeouts). **Plan the first deploy around hour 3 of the event**, even if `/ask` still returns 501. That way you surface infrastructure issues with hours of buffer, and a Yellow Tech mentor can help if needed.

Once both services are live, every subsequent `railway up` takes seconds.

## Useful CLI commands

```bash
railway whoami                                 # verify which account is logged in
railway status                                 # show project + linked service
railway service <name>                         # link CLI to a specific service
railway list                                   # list your projects
railway logs                                   # tail runtime logs of the linked service
railway logs --build                           # build logs (useful when deploy fails)
railway variables                              # list env vars on the linked service
railway variables --set NAME=value             # set or update an env var
railway domain                                 # generate or print the public URL
```

## Common issues

| Issue | Fix |
|---|---|
| `railway: command not found` | `npm install -g @railway/cli` |
| `No service could be found` | After `railway up --detach` the CLI loses the link. Run `railway service <name>` (default service name = project name). Or use plain `railway up` to keep the link. |
| Backend build fails on `uv sync` | Check that `pyproject.toml` is valid. Most often: a typo in deps. See logs with `railway logs --build` |
| Backend healthcheck failing | Make sure `GET /health` returns `{"status":"ok"}` (already in template). Increase `healthcheckTimeout` in `backend/railway.json` if your build takes long to warm up. |
| `/ask` returns 401 (OpenAI) | Re-set: `railway variables --set OPENAI_API_KEY=sk-...` |
| Frontend can't reach backend | Confirm `VITE_BACKEND_URL` was set **before** the frontend build (Vite inlines it at build time), and points to the backend's public URL with `https://`. After changing the var, redeploy: `railway up`. |
| CORS error in browser console | Either set `FRONTEND_URL` on backend, or leave it unset (defaults to `*`) |
| Cold start timeout | Free tier sleeps after inactivity. First request after sleep takes ~30s |
| `railway domain` already exists | Idempotent - it just prints the existing one. To delete and regenerate, use the dashboard. |
| `Blocked request. This host is not allowed` (frontend) | Vite preview blocks unknown hosts for security. The starter's `vite.config.ts` already has `preview: { allowedHosts: true }` to bypass this on Railway. If you removed it, add it back. |
| `railway up` upload is huge (>100MB) or stalls | A `venv/` (no leading dot) or `env/` folder is being uploaded. Railway auto-excludes `.venv` (with the dot) but NOT the `venv` / `env` variants. Either rename your virtual env to `.venv`, or rely on the `.dockerignore` shipped with the starter (root + `backend/`). |
| Service deployed in US but you wanted EU | `railway scale --service <name> --europe-west4=1` redeploys it in EU. Set Account Settings -> Default Region = EU before any future `railway init`. |
| OpenAI 429 / "tokens per minute exceeded" under load | Your model is rate-limiting. First move: switch to a sibling model (older snapshots throttle harder). Second: add retry-with-backoff. See `AGENTS.md` -> "When the LLM call errors out". |
| Healthcheck timeout right after deploy | The backend is doing too much at startup (probably embedding the corpus). It must NOT - prebuild the index locally and ship it. See `AGENTS.md` -> "Embedding strategy". |

## Setting environment variables - two ways

**Via CLI** (works fine, Codex can do this for you):
```bash
railway variables --set OPENAI_API_KEY=sk-...
railway variables --set FRONTEND_URL=https://buddy-frontend-yourname.up.railway.app
```

**Via dashboard**: open the project → click the service → Variables tab → "+ New Variable". Same effect, more visual.

Both auto-trigger a redeploy if the variable changes. For the frontend's `VITE_BACKEND_URL`, you must redeploy with `railway up` even after setting it (because Vite inlines it at build time, not at runtime).

## Adding a database (optional, for differentiation)

For the AI Buddy itself you do NOT need a database. The RAG index lives on disk inside the production image (see `AGENTS.md` -> "Embedding strategy"). Add Postgres only if you want to:

- **Log every Q/A pair** the buddy answers - great Level 2 demo material ("look, here are the most-asked questions today").
- **Cache identical incoming questions** to dodge the 30-second budget on repeats.
- **Power a small analytics view** on the frontend (verticale split, response-time histogram).

### Steps from the dashboard

1. Project page -> **+ New** -> **Database** -> **Postgres**.
2. Wait ~30 seconds. Postgres comes up with `pgvector` already enabled (no need to run `CREATE EXTENSION` yourself).
3. Railway auto-injects `DATABASE_URL` and a few sibling vars (`PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`) into your **backend** service. The backend redeploys once to pick them up.
4. Connect from Python:

```python
import os
import psycopg

conn = psycopg.connect(os.environ["DATABASE_URL"])
```

Or via SQLAlchemy:

```python
from sqlalchemy import create_engine
engine = create_engine(os.environ["DATABASE_URL"])
```

From CLI, the same in one line: `railway add --plugin postgresql`.

### Two gotchas

- **Region**: the Postgres service deploys in the same region as your backend at the time of creation. If you set EU as your default region first (see above), the DB lands in EU too.
- **Hard fail on missing `DATABASE_URL`**: if you add Postgres mid-event, the backend redeploys with the new env var. If your code raises on import when `DATABASE_URL` is missing, your previous deploy may have already been broken silently. Wrap the connection in `try / except`, or feature-flag it behind an `if "DATABASE_URL" in os.environ:` check.

---

## Codex prompt - let the agent handle it

Paste this into Codex Desktop App when you're ready to deploy:

```
Deploy this project to Railway as two services (backend + frontend). Steps:

1. Verify the Railway CLI is installed (`railway --version`). If not,
   tell me to install it with `npm install -g @railway/cli`.

2. Run `railway login` and wait for me to confirm I've completed the
   browser auth flow.

3. BEFORE creating the project, tell me to set my Account default
   region to "EU West Metal (Amsterdam)" in railway.com -> Account
   Settings -> Default Region. The event runs in Europe; EU region
   means lower latency vs the 30s budget. Wait for me to confirm.

4. From the project root, run `railway init` to create a new Railway
   project. Use a sensible name like "bocconi-buddy-mine".

BACKEND:
5. Cd into backend/, run `railway up`. Railway will build
   from backend/Dockerfile. The starter ships a `.dockerignore` in
   backend/ that excludes venv/, env/, caches and editor files - if
   the upload looks suspiciously big, double-check no large folder
   slipped in.

6. Ask me for my OpenAI API key (the `sk-...` I generated after
   redeeming my code on platform.openai.com - not the redemption
   code itself), then set it: `railway variables --set
   OPENAI_API_KEY=...` while still in the backend service context.

7. Run `railway domain` to generate the public URL of the backend.
   Save it - I'll need it for the frontend.

8. Smoke-test:
   curl https://<backend-url>/health
   curl -X POST https://<backend-url>/ask -H 'Content-Type: application/json' \
     -d '{"question":"test"}'

FRONTEND:
9. Cd into frontend/. Create a second service in the same project
   (use the dashboard if needed, or `railway service create`).

10. Set the env var so the frontend knows where the backend is:
    `railway variables --set VITE_BACKEND_URL=https://<backend-url>`

11. Run `railway up`. Railway runs `npm install && npm run build`,
    then serves the build with `vite preview`.

12. Run `railway domain` to generate the public frontend URL.

VERIFY:
13. Visit the frontend URL in a browser, confirm it loads.
14. Test the chat flow: type a question, confirm the frontend reaches the backend.
15. If anything errors out, check `railway logs` and surface the issue
    in plain language. For OpenAI rate limits, the fix is usually
    "switch model family" - websearch the current OpenAI lineup if
    your training data is older than the event date.
16. Report both URLs back to me. The BACKEND URL is what we submit to the
    hackathon form.
```
