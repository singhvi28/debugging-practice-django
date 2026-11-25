# Expense Reports (Django)

Practice debugging a small expense report workflow API.

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

Mutating endpoints expect: `Authorization: Bearer secret-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/reports` | No |
| GET | `/reports/{report_id}` | No |
| POST | `/reports` | Yes |
| POST | `/reports/{report_id}/submit` | No |
| POST | `/reports/{report_id}/approve` | Yes |
| POST | `/reports/{report_id}/lines` | Yes |
