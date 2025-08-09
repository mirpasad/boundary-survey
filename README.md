# Boundary Survey — AI Survey Generator

Monorepo with a React frontend and a FastAPI backend that generates surveys from a short description, caches by prompt, and returns a UI-friendly schema.

## Structure
- `frontend/` React app
- `backend/` FastAPI service

## Quick start (docker)
```bash
cp .env.example .env
docker compose up --build
# API at http://localhost:8000  |  Frontend at http://localhost:3000 (after we wire it)
