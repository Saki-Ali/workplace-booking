# Workplace Booking MVP

Lightweight desk booking proof-of-concept with a FastAPI backend and a Vite/React/Tailwind frontend. Uses SQLite and mock login to demonstrate core flows: view desks, see availability, book/cancel, and browse a simple floorplan.

## Project Structure
- `backend/` - FastAPI app, SQLite via SQLAlchemy, seed data for 10 desks.
- `frontend/` - Vite + React + TypeScript + Tailwind UI with Zustand store.
- `docker-compose.yml` - One-step local run for frontend + backend.

## How It Works
- Backend exposes `/login`, `/workplaces`, `/bookings` (list/create/delete). On startup it seeds 10 desks into `app.db`. CORS is open for local dev.
- Frontend uses a simple login (any name), stores session in Zustand (persisted), calls the API for workplaces/bookings, and renders pages: login, dashboard, workplaces list, floorplan, bookings.
- Floorplan is a clickable SVG grid; booking buttons toggle via API calls.

## Run Locally (without Docker)
Prereqs: Python 3.11+, Node 18+, npm.

Create a virtual environment (recommended):
- Windows (PowerShell):
  ```powershell
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
- Linux/macOS:
  ```bash
  cd backend
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

Start backend:
```bash
uvicorn backend.main:app --reload
# API at http://localhost:8000
```

Start frontend (new shell):
```bash
cd frontend
npm install
npm run dev
# App at http://localhost:5173
```

## Run with Docker Compose (recommended)
1) Install Docker Desktop (Windows/macOS) or Docker Engine + Docker Compose plugin (Linux).
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - macOS: https://docs.docker.com/desktop/install/mac-install/
   - Linux engine: https://docs.docker.com/engine/install/ and compose plugin: https://docs.docker.com/compose/install/linux/
2) From repo root:
   ```bash
   docker compose up --build
   ```
   (If your Docker requires the hyphenated command, use `docker-compose up --build`.)

Services:
- Frontend: http://localhost:5173
- Backend:  http://localhost:8000

## Build/Run Images Manually
Backend:
```bash
docker build -t workplace-backend ./backend
docker run -p 8000:8000 -v ${PWD}/backend/app.db:/app/backend/app.db workplace-backend
```

Frontend:
```bash
docker build -t workplace-frontend ./frontend
docker run -p 5173:4173 workplace-frontend
```

## API Quick Peek
- `POST /login` -> `{ "username": "Alice" }` returns dummy token.
- `GET /workplaces` -> list desks with `is_booked` + `booking_id`.
- `POST /bookings` -> `{ "workplace_id": 1, "user": "Alice" }` creates booking.
- `DELETE /bookings/{id}` -> cancel booking.

Example:
```bash
curl http://localhost:8000/workplaces
curl -X POST http://localhost:8000/bookings -H "Content-Type: application/json" -d '{\"workplace_id\":1,\"user\":\"Alice\"}'
```

## Notes
- SQLite file lives at `backend/app.db` when run from the repo, or `/app/backend/app.db` in containers (mounted via compose).
- No environment variables are required for this MVP.
