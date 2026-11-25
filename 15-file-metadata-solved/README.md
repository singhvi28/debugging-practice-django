# File Metadata (Django)

Practice debugging a small file tagging service API.

## Setup

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

## Run locally

```bash
python manage.py runserver
```

## Auth

Protected endpoints expect: `Authorization: Bearer secret-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/api/files` | No |
| GET | `/api/files/{file_id}` | No |
| POST | `/api/files` | Yes |
| PATCH | `/api/files/{file_id}` | Yes |
| POST | `/api/files/{file_id}/tags` | Yes |
