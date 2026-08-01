# 🎙️ PodLens

AI-powered podcast analytics dashboard — track performance across Spotify,
YouTube & Apple Podcasts in one place.

This is the **simplified single-tenant build**: a full, locally-runnable MVP
with no accounts, no login, and no API keys required. It ships with
mock-seeded analytics so every chart renders immediately.

## Stack

| Layer     | Tech                                           |
| --------- | ---------------------------------------------- |
| Frontend  | React + Vite + Recharts + React Router         |
| Backend   | Django + Django REST Framework                 |
| App data  | PostgreSQL (podcasts, episodes)                |
| Analytics | ClickHouse (high-volume events)                |
| Pipeline  | Prefect (mock-data flow; real ingestion later) |
| AI        | Claude API (insights — stubbed until a key is set) |

## No authentication

PodLens is **single-tenant and unauthenticated**. There is no signup, no
login, no session or token handling, and no user table — every podcast
belongs to the instance, and every API endpoint is open.

That makes it a great local/demo tool and a poor fit for the public internet
as-is. Anyone who can reach the API can read and modify all data. If you
deploy it, put it behind a network boundary you control (VPN, private
network, or an authenticating reverse proxy).

The Django admin is also gone, since it is an auth-gated login backed by
`django.contrib.auth`. Manage podcasts and episodes through the REST API.

## Prerequisites

- Docker + Docker Compose
- Python 3.11+
- Node 18+

## Ports

To avoid colliding with other local stacks, PodLens publishes its databases on
non-standard host ports (the containers themselves use the defaults internally):

| Service          | Host port | Container port |
| ---------------- | --------- | -------------- |
| PostgreSQL       | `5433`    | 5432           |
| ClickHouse HTTP  | `8124`    | 8123           |
| ClickHouse native| `9001`    | 9000           |

The compose project name is `podlens`, so its containers, network, and volumes
stay isolated from any other Docker projects. `.env.example` already points the
backend at `5433` / `8124`.

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

Open http://localhost:5173. You land straight on the Dashboard with populated
charts, an Episodes table, and a working AI Insights button — no sign-in step.

## Enabling live Claude insights

By default `POST /api/insights/generate` returns a clearly-labeled stub so the
app runs with zero credentials. To enable real Claude analysis, set
`ANTHROPIC_API_KEY` in `backend/.env` and restart the server. No other changes
needed.

## API overview

Every endpoint is open — no headers, no tokens.

| Method | Endpoint                   | Purpose                          |
| ------ | -------------------------- | -------------------------------- |
| GET    | `/`                        | JSON index of every endpoint     |
| GET    | `/api/health`              | Liveness check                   |
| CRUD   | `/api/podcasts/`           | Manage podcasts                  |
| CRUD   | `/api/episodes/`           | Manage episodes                  |
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

- Real Spotify / YouTube / Apple ingestion
- Live Claude insights in production
- Deploy to DigitalOcean behind a private network
- React Native mobile app (only if users ask)
