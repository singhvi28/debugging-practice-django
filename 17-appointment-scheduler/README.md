# Appointment Scheduler (Django)

Practice debugging provider scheduling and appointment booking.

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

Protected mutating routes: `Authorization: Bearer secret-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/providers` | No |
| GET | `/providers/{provider_id}` | No |
| POST | `/appointments` | Yes |
| GET | `/appointments?date=YYYY-MM-DD` | No |
| GET | `/appointments/{appointment_id}` | No |
| PATCH | `/appointments/{appointment_id}` | Yes |
| POST | `/appointments/{appointment_id}/cancel` | Yes |
