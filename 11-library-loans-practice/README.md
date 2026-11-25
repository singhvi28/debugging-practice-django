# Library Loans (Django)

Practice debugging a small library service API for books and loans.

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

Most mutating endpoints expect: `Authorization: Bearer secret-token`

Staff-only endpoints expect: `Authorization: Bearer admin-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/books` | No |
| GET | `/books/{book_id}` | No |
| POST | `/loans` | Yes |
| GET | `/loans` | No |
| GET | `/loans/overdue` | Admin |
| POST | `/loans/{loan_id}/return` | No |
