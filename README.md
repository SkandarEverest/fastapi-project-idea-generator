# FastAPI Project Idea Generator (Jinja Form + Structured Result)

## Features
- GET `/` serves HTML form (Jinja2)
- POST `/result` returns:
  - HTML (default) or
  - JSON (if `format=json`)
- Healthcheck: GET `/health`
- Swagger: `/docs`

## Setup
```bash
pip install uv
uv venv
source .venv/bin/activate
uv sync
cp .env.example .env
# edit .env: set OPENAI_API_KEY
