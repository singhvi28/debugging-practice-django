# Event Tickets (Django)

Practice debugging a small event ticketing API with bookings and cancellations.

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

Protected routes expect:

```text
Authorization: Bearer secret-token
```

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/events?search=` | No |
| GET | `/events/{event_id}` | No |
| POST | `/events` | Yes |
| POST | `/events/{event_id}/tickets` | Yes |
| GET | `/tickets/{ticket_id}` | No |
| DELETE | `/tickets/{ticket_id}` | Yes |
