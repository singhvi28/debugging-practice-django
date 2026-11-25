# Forum Threads (Django)

Practice debugging a small forum API with threads and replies.

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
| GET | `/threads` | No |
| GET | `/threads/{thread_id}` | No |
| GET | `/threads/deleted` | No |
| POST | `/threads` | Yes |
| POST | `/threads/{thread_id}/replies` | No |
| DELETE | `/threads/{thread_id}/replies/{reply_id}` | Yes |
