# AI Food Logistics System

[![CI](https://github.com/maverick0721/AI-Food-Logistics-System/actions/workflows/ci.yml/badge.svg)](https://github.com/maverick0721/AI-Food-Logistics-System/actions/workflows/ci.yml)

An end-to-end experimentation platform for intelligent food delivery operations. The repository combines a FastAPI backend, Kafka-based event flow, PostgreSQL persistence, a React dashboard, and a set of ML and simulation modules for routing, ETA prediction, demand modeling, and dispatch experimentation.

The goal of the project is straightforward: make it easy to model, run, and improve a food logistics system without splitting the work across multiple disconnected repositories.

## What This Repository Covers

- Order intake and restaurant management through a FastAPI backend
- Kafka event publishing and consumption for order-driven workflows
- PostgreSQL-backed persistence for operational entities
- A React dashboard for monitoring, order creation, recommendation checks, and map-based awareness
- Research modules for graph routing, ETA prediction, demand forecasting, RL dispatch, and simulation
- CI checks for backend tests, import integrity, frontend tests, and frontend production builds

## System At A Glance

```mermaid
flowchart LR
	UI[React Dashboard] --> API[FastAPI Backend]
	API --> DB[(PostgreSQL)]
	API --> KAFKA[(Kafka Broker)]
	KAFKA --> CONSUMER[Dispatch Consumer]
	API --> REC[Recommendation Service]
	API --> DISP[Dispatch Service]
	DISP --> RL[Policy Model]
	REC --> MLS[ML Recommendation Model]
```

## Architecture

The backend is the operational core. It exposes endpoints for orders, restaurants, dispatch, recommendation, and dashboard metrics. Order creation writes to PostgreSQL and publishes an `ORDER_CREATED` event to Kafka. A consumer listens to that stream and can trigger downstream dispatch-oriented workflows. Around that operational path, the repository also contains simulation and learning modules used to train, benchmark, and iterate on logistics strategies.

```mermaid
flowchart TD
	subgraph Frontend
		A[React App]
		M[Map View]
		KPI[Live KPI Cards]
	end

	subgraph Platform
		B[FastAPI App]
		R1[Order Router]
		R2[Restaurant Router]
		R3[Recommendation Router]
		R4[Delivery Router]
		R5[Metrics Router]
	end

	subgraph Data and Events
		P[(PostgreSQL)]
		K[(Kafka)]
		C[Dispatch Consumer]
	end

	subgraph Intelligence
		G[Graph Engine]
		E[ETA / Recommendation Models]
		D[RL Dispatch]
		S[Simulator]
	end

	A --> B
	M --> A
	KPI --> A
	B --> R1
	B --> R2
	B --> R3
	B --> R4
	B --> R5
	R1 --> P
	R2 --> P
	R1 --> K
	K --> C
	R3 --> E
	R4 --> D
	D --> S
	E --> G
```

## Core Runtime Workflow

```mermaid
sequenceDiagram
	participant User
	participant Frontend
	participant API
	participant Postgres
	participant Kafka
	participant Consumer
	participant Dispatch

	User->>Frontend: Create order
	Frontend->>API: POST /orders
	API->>Postgres: Insert order
	API->>Kafka: Publish ORDER_CREATED
	API-->>Frontend: Return created order
	Kafka-->>Consumer: Deliver event
	Consumer->>Dispatch: Trigger dispatch logic
```

## Repository Layout

```text
backend/          FastAPI application, routers, services, streaming logic, database models
frontend/         React dashboard and UI tests
graph_engine/     Routing, graph building, and graph learning modules
ml_models/        Recommendation, ETA, and forecasting model code
rl_dispatch/      Reinforcement learning environment and training code
mega_simulator/   Large-scale simulation components
training/         Shared policy model and training scripts
data_pipeline/    Dataset ingestion and processing
evaluation/       Evaluation scripts for model behavior
infra/            Docker, Kubernetes, Kafka helper scripts, monitoring config
scripts/          One-command local system startup and shutdown helpers
tests/            Backend smoke tests and config tests
docs/             Architecture notes
```

## Local Development

### 1. Environment Setup

```bash
git clone https://github.com/maverick0721/AI-Food-Logistics-System.git
cd AI-Food-Logistics-System
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

If `requirements.txt` is intentionally lightweight in your environment, install only the packages you need for the path you are testing.

### 2. Start the Full Local Stack

The repository includes helper scripts for local development that start Kafka, ZooKeeper, PostgreSQL, FastAPI, and the dispatch consumer.

```bash
./scripts/start_full_system.sh
```

Available local endpoints after startup:

- API: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- PostgreSQL: `127.0.0.1:5432`
- Kafka: `127.0.0.1:9092`

To stop everything:

```bash
./scripts/stop_full_system.sh
```

### 3. Start the Frontend

From the frontend directory:

```bash
cd frontend
npm install
npm start
```

The dashboard runs on port `3000` by default.

For Mapbox rendering, define a token in `frontend/.env`:

```bash
REACT_APP_MAPBOX_TOKEN=your_public_mapbox_token
```

## Frontend Experience

The frontend is designed as a lightweight operations console rather than a marketing site. It includes:

- A modern dashboard layout with a day/night theme toggle
- Live KPI cards backed by backend metrics
- Order creation and recommendation panels
- Restaurant list overview
- Delivery map panel with safe fallback behavior if the map cannot initialize

## API Surface

Key endpoints currently exposed by the backend:

- `GET /`
- `GET /orders`
- `POST /orders`
- `GET /restaurants`
- `POST /restaurants`
- `GET /recommend?user_id=...&restaurant_id=...`
- `POST /dispatch/{order_id}`
- `GET /metrics/dashboard`

## Testing and Quality Checks

Backend:

```bash
pytest -q
```

Frontend tests:

```bash
cd frontend
CI=true npm test -- --watchAll=false --runInBand
```

Frontend production build:

```bash
cd frontend
npm run build
```

The CI workflow runs:

- Backend tests
- Backend syntax check
- Backend import sweep
- Frontend tests
- Frontend production build

## Infrastructure Notes

The repository includes Docker, Docker Compose, Kubernetes, and monitoring manifests under `infra/`, but whether those can be executed depends on the host environment.

For example, some remote notebook or sandbox environments do not expose a usable Docker daemon or Kubernetes tooling. In those cases, the shell scripts in `scripts/` are the intended local runtime path.

## Design Principles Behind The Repo

This codebase is opinionated in a useful way:

- Keep operational workflows runnable without heavy orchestration when possible
- Keep ML, simulation, and serving code close enough to evolve together
- Prefer clear local scripts for development before optimizing deployment paths
- Test the system at the seams: API, events, imports, and frontend build stability

## Roadmap-Friendly Areas

There are several natural directions for expansion:

- richer recommendation and ETA metrics
- real dispatch dashboards tied directly to stream state
- stronger simulator-to-model feedback loops
- deeper observability with Prometheus and runtime traces
- production deployment hardening for containerized environments

## License / Usage

Add your preferred license here if you intend to open-source the project publicly.
