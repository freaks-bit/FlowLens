# FlowLens

**Facility occupancy monitoring, sensor status, and operational alerts — in one dashboard.**

FlowLens is a full-stack smart-space analytics project that converts visitor **IN/OUT counting events** into zone-level occupancy, facility utilization, historical trends, sensor-activity health, and configurable alerts. It is designed as a practical example of an operations dashboard for places such as shopping malls, offices, and other managed facilities.

> **Demonstration notice:** The publicly hosted FlowLens facility, sensors, and visitor events are **simulated**. No physical counting sensors are connected. Occupancy represents the *last recorded event-derived count*, not a verified live headcount.

**[Live dashboard](https://flowlens-sand.vercel.app)** · **[API documentation](https://flowlens-api-uz68.onrender.com/docs)** · **[API health](https://flowlens-api-uz68.onrender.com/api/v1/health)**

## Features

- **Facility overview:** Total recorded occupancy, configured zone capacity, available capacity, and utilization percentage.
- **Zone monitoring:** Individual occupancy, availability, and utilization for each monitored area.
- **Historical analytics:** Event-derived occupancy charts with zone selection and 24-hour, 7-day, 14-day, and 30-day views.
- **Visitor event feed:** Recent arrivals (`IN`) and departures (`OUT`), attributed to a sensor and zone.
- **Configurable occupancy alerts:** Rules with thresholds, including utilization-based advisories displayed when triggered.
- **Sensor health:** Per-sensor reported status and last-event freshness, with recent/stale summaries. Event freshness does not prove physical connectivity.
- **REST API:** Endpoints for managing facilities, zones, sensors, counting events, and alert rules, plus analytics and health endpoints.
- **Public demonstration:** React frontend on Vercel, FastAPI backend on Render, and PostgreSQL hosted by Neon.

## Demo dataset

The hosted demo models a fictional **FlowLens Demo Mall** with the following *synthetic* data:

| Item | Demo configuration |
| --- | ---: |
| Zones | 2 — Main Entrance and Food Court |
| Simulated sensors | 2 |
| Simulated visitor events | 284 |
| Configured alert rules | 3 |
| Main Entrance capacity | 350 |
| Food Court capacity | 500 |
| Total configured capacity | 850 |

At the time the demo was seeded, the last recorded occupancy was **42** at the Main Entrance and **54** at the Food Court, totaling **96 people** (**11.29%** overall utilization). These are sample records, not measurements of a real location. Sensor freshness indicators may change as the dataset ages.

## Technology stack

| Layer | Technologies | Purpose |
| --- | --- | --- |
| Frontend | React, TypeScript, Vite, Recharts | Dashboard UI, typed API integration, and charts |
| Backend | Python, FastAPI, Pydantic | Validated REST endpoints and business logic |
| Data access | SQLAlchemy, psycopg | ORM and PostgreSQL connectivity |
| Database | PostgreSQL | Relational storage for facility configuration and event records |
| Migrations | Alembic | Version-controlled database schema changes |
| Hosting | Vercel, Render, Neon | Frontend, API, and hosted PostgreSQL |
| Development | VS Code, Git, GitHub, Swagger UI | Coding, version control, and API exploration |

## System architecture

```text
 Browser
   |
   v
 React + TypeScript dashboard (Vercel)
   |
   | HTTPS / REST (JSON)
   v
 FastAPI application (Render)
   |-- API routers and Pydantic validation
   |-- Services: occupancy, history, alerts, sensor health
   |-- Repositories: database queries
   |
   v
 SQLAlchemy + psycopg
   |
   v
 PostgreSQL database (Neon)
   |-- Sites and zones
   |-- Sensors and count events
   `-- Alert rules
```

**Occupancy calculation:** An `IN` event contributes a positive count and an `OUT` event contributes a negative count. The backend aggregates these events by sensor and zone to reconstruct occupancy. Historical views account for events preceding the selected time window so the chart starts with the appropriate baseline.

**Alert evaluation:** A zone can have configurable rules, such as an advisory when utilization reaches a specified percentage. Configurable alert rules are separate from the dashboard's general normal/warning/critical zone status.

## Project structure

```text
FlowLens/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # API route handlers
│   │   ├── core/           # Application settings
│   │   ├── db/             # Database engine and sessions
│   │   ├── models/         # SQLAlchemy models
│   │   ├── repositories/   # Database queries
│   │   ├── schemas/        # Pydantic request/response models
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── seed_demo.py        # Synthetic hosted-demo seed utility
├── frontend/
│   ├── src/
│   │   ├── components/    # Dashboard panels and charts
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript interfaces
│   └── package.json
└── README.md
```

## Run locally

Prerequisites: Python, Node.js/npm, and a running PostgreSQL database. Commands below use **Windows PowerShell** and assume the repository is checked out locally.

### 1. Backend

```powershell
git clone https://github.com/freaks-bit/FlowLens.git
cd FlowLens\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `backend/.env` with your own PostgreSQL connection settings. For example:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flowlens
DB_USER=flowlens_app
DB_PASSWORD=YOUR_LOCAL_DATABASE_PASSWORD
DB_SSLMODE=prefer
DEMO_READ_ONLY=false
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Use your actual local database name, username, and password. **Never commit `.env` or credentials.** With the database available, apply the existing schema and start the API:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger API documentation.

### 2. Frontend

Open a **second** PowerShell terminal at the **repository root** (`FlowLens/`):

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Ensure `frontend/.env.local` contains:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Open **http://localhost:5173** to view the dashboard. The backend and frontend must both be running.

### 3. Frontend checks

```powershell
npm run lint
npm run build
```

## Selected API endpoints

The API documentation at `/docs` contains the full request and response schemas. Representative routes include:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | API and database connection health |
| `GET` | `/api/v1/sites/{site_id}/occupancy` | Facility totals and zone summaries |
| `GET` | `/api/v1/zones/{zone_id}/occupancy` | Zone occupancy and triggered alerts |
| `GET` | `/api/v1/zones/{zone_id}/history` | Occupancy history for a time window |
| `GET` | `/api/v1/sites/{site_id}/sensor-health` | Sensor event-freshness monitoring |
| `GET` | `/api/v1/events/recent` | Recent visitor counting events |
| `GET` | `/api/v1/zones/{zone_id}/alert-rules` | Configured rules for a zone |
| `POST` | `/api/v1/sensors/{sensor_id}/events` | Ingest an `IN` or `OUT` count event in writable environments |

The public demonstration is intended for viewing and should be kept in **read-only mode**; use a local development environment to exercise mutation endpoints.

## Engineering decisions and limitations

- **Layered backend design:** Route handlers, validation schemas, services, and repositories are separated to keep responsibilities clear.
- **Database migrations:** Alembic provides a repeatable schema setup process for local and hosted PostgreSQL.
- **Time-window baseline:** Historical analytics reconstructs a zone's occupancy from events before and within the selected range.
- **Explicit sensor freshness:** A sensor marked `online` can still be stale if it has not submitted an event recently; this distinction is shown in the UI.
- **Synthetic, not physical telemetry:** Events are seeded for demonstration, so the dashboard does not claim to measure an actual building.
- **Last-recorded rather than guaranteed real-time:** Values only change when new count events are ingested; without continuous hardware feeds, the demo is not a live tracking system.

## Deployment

| Component | Service | Address |
| --- | --- | --- |
| Dashboard | Vercel | [flowlens-sand.vercel.app](https://flowlens-sand.vercel.app) |
| REST API | Render | [flowlens-api-uz68.onrender.com](https://flowlens-api-uz68.onrender.com) |
| PostgreSQL | Neon | Managed database; credentials are private |

The frontend uses `VITE_API_BASE_URL` for the API address. The backend uses environment variables for PostgreSQL, SSL, public-demo write protection, and allowed CORS origins. Hosting on a free tier may introduce a cold-start delay after inactivity.

## Author

Built as a hands-on full-stack portfolio project to demonstrate REST API development, relational data modeling, operational dashboards, deployment, and end-to-end integration.
