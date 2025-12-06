# Ads-Project

## Overview

This project is a recommender system web application of movies.

## Main components

- Backend: `src/api` — FastAPI application with SQLAlchemy models, Alembic migrations, and seed data.
- Frontend: `web` — React application using TypeScript and Vite.
- PostgreSQL: Database

## How to run (quick)

1) Using Docker (recommended)

```bash
docker-compose up --build
```

This starts backend and frontend containers. Default ports:

- Backend: `http://localhost:5005`
- Frontend: `http://localhost:80`

2) Run backend locally (no Docker)

```bash
cd src/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Apply migrations:

```bash
cd src/api
alembic upgrade head
```

Seed database (if needed):

```bash
python seed_data.py
```

3) Run frontend locally

```bash
cd web
npm install
npm run dev
```

4) Run tests

- Backend tests: `cd src/api && pytest`

## CI/CD is set up with GitLab CI to automate:

- Running static code analysis (linters)
- Running unit tests
- Building and pushing Docker images to the registry
- Automated documentation generation and deployment
- Deploying to production environments
