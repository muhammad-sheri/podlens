# 🎙️ PodLens

AI-powered podcast analytics dashboard — track performance across Spotify,
YouTube & Apple Podcasts in one place.

This is the **Phase 1 web app**: a full, locally-runnable MVP scaffold. It ships
with mock-seeded analytics so every chart renders immediately — no third-party
API keys required.

## Stack

| Layer     | Tech                                           |
| --------- | ---------------------------------------------- |
| Frontend  | React + Vite + Recharts + React Router         |
| Backend   | Django + Django REST Framework + SimpleJWT     |
| App data  | PostgreSQL (users, podcasts, episodes)         |
| Analytics | ClickHouse (high-volume events)                |
| Pipeline  | Prefect (mock-data flow; real ingestion later) |
| AI        | Claude API (insights — stubbed until a key is set) |

## Prerequisites

- Docker + Docker Compose
- Python 3.11+
- Node 18+

## Quick start

```bash
# 1. Start the databases
docker compose up -d

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env          # adjust if needed
python manage.py migrate
python manage.py seed_demo       # seeds Postgres + ClickHouse with demo data
python manage.py runserver       # API at http://localhost:8000

# 3. Frontend (in a second terminal)
cd frontend
npm install
npm run dev                      # UI at http://localhost:5173
```

Open http://localhost:5173 and sign in with the seeded demo account:

- **email:** `demo@podlens.app`
- **password:** `podlens-demo`

You'll land on the Dashboard with populated charts, an Episodes table, and a
working AI Insights button.

## Enabling live Claude insights

By default `POST /api/insights/generate` returns a clearly-labeled stub so the
app runs with zero credentials. To enable real Claude analysis, set
`ANTHROPIC_API_KEY` in `backend/.env` and restart the server. No other changes
needed.

## API overview

| Method | Endpoint                   | Purpose                          |
| ------ | -------------------------- | -------------------------------- |
| POST   | `/api/auth/register`       | Create an account                |
| POST   | `/api/auth/login`          | Obtain JWT access + refresh      |
| POST   | `/api/auth/refresh`        | Refresh access token             |
| GET    | `/api/auth/me`             | Current user                     |
| CRUD   | `/api/podcasts/`           | Manage podcasts (per user)       |
| CRUD   | `/api/episodes/`           | Manage episodes (per user)       |
| GET    | `/api/analytics/overview`  | Totals + downloads/listeners series |
| GET    | `/api/analytics/platforms` | Platform breakdown               |
| GET    | `/api/analytics/episodes`  | Per-episode rollups              |
| POST   | `/api/insights/generate`   | AI insight (stub or live Claude) |

## Data pipeline

`backend/pipeline/seed.py` generates ~90 days of realistic analytics. It runs via
`python manage.py seed_demo` or standalone (`python pipeline/seed.py`). The same
logic is wrapped in a Prefect flow at `backend/pipeline/flows.py`
(`python pipeline/flows.py`) — the orchestration pattern that real Spotify /
YouTube / Apple ingestion will plug into in a later phase.

## Roadmap (later phases)

- Real Spotify / YouTube / Apple ingestion + OAuth
- Live Claude insights in production
- Deploy to DigitalOcean; first paying users
- React Native mobile app (only if users ask)
