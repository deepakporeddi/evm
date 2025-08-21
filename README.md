Event-Management Project - Async SQLModel (Postgres + Docker)

This repo is patched to use async SQLModel with asyncpg (Postgres) and includes Docker + docker-compose.

Quickstart (Docker):
1. docker compose up --build -d
2. API: http://localhost:8000/api, Swagger: http://localhost:8000/docs

Local quickstart:
1. python -m venv .venv; source .venv/bin/activate
2. pip install -r requirements.txt
3. export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/evm"
4. uvicorn evm.src.main:app --reload
Event Management API (FastAPI + SQLAlchemy, Async)

A minimal, clean-architecture Event Management backend with FastAPI and async SQLAlchemy.

Features:

Create events (name, location, start/end time, max capacity)

List upcoming events

Register attendees to events

Prevent overbooking (capacity enforcement)

Prevent duplicate registrations per event (unique constraint)

Prevent duplicate attendee emails globally

List attendees for an event with pagination

Timezone handling:

Store times in UTC

Assume inputs are in Asia/Kolkata (IST) by default if naive \
Convert to any timezone on reads via tz query param (default Asia/Kolkata) \

Proper separation: routers (HTTP), services (business logic), models (ORM), schemas (IO)

OpenAPI/Swagger at /docs

Unit tests with pytest + httpx


Stack:
FastAPI \
SQLAlchemy 2.0 (async) with SQLite (aiosqlite) by default (works with PostgreSQL by setting DATABASE_URL) \
Pydantic v2 \
Pytest \

Setup:
python -m venv .venv \
source .venv/bin/activate \
pip install -r requirements.txt \
export DATABASE_URL="sqlite+aiosqlite:///./events.db"  # optional; defaults to sqlite

uvicorn app.main:app --reload \
Open http://127.0.0.1:8000/docs for Swagger UI.

API: \
Create Event: 
```bash
curl -X POST http://127.0.0.1:8000/events  -H "Content-Type: application/json"  -d '{
  "name": "Tech Meetup",
  "location": "Hyderabad",
  "start_time": "2025-08-25T18:00:00",
  "end_time": "2025-08-25T20:00:00",
  "max_capacity": 2
 }'
If start_time/end_time are naive, they're interpreted as IST and stored in UTC.
```
List Upcoming Events (timezone-aware)
```bash
curl "http://127.0.0.1:8000/events?tz=UTC"
```
Register Attendee \
```bash
curl -X POST http://127.0.0.1:8000/events/1/register  -H "Content-Type: application/json"  -d '{"name":"Alice","email":"alice@example.com"}'
```
List Attendees (pagination) \
```bash
curl "http://127.0.0.1:8000/events/1/attendees?page=1&page_size=10"
```
Timezone Notes \
All event times are stored in UTC. \
On create, naive datetimes are assumed to be Asia/Kolkata and converted to UTC. \
On read, pass ?tz=America/New_York (or any tz database name) to get localized times. \
Default output tz is Asia/Kolkata to match the requirement. \

**Migrations / Schema** \
Run migrations with Alembic:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

