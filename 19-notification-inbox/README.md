# Notification Inbox (Django)

Practice debugging notification read state and unread counts.

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

All routes require `Authorization: Bearer secret-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/notifications` | Yes |
| GET | `/notifications/unread-count` | Yes |
| GET | `/notifications/{notification_id}` | Yes |
| POST | `/notifications` | Yes |
| POST | `/notifications/{notification_id}/read` | Yes |
| POST | `/notifications/mark-all-read` | Yes |
