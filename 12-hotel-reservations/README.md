# Hotel Reservations (Django)

Practice debugging a small hotel booking service API.

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
| GET | `/rooms` | No |
| GET | `/rooms/{room_id}` | No |
| GET | `/bookings` | No |
| POST | `/bookings` | Yes |
| DELETE | `/bookings/{booking_id}` | Yes |
