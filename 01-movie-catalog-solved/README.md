# Movie Catalog (Django)

Practice debugging a small movie catalog API with reviews and watchlists.

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
| GET | `/movies?search=` | No |
| GET | `/movies/{movie_id}` | No |
| POST | `/movies` | Yes |
| DELETE | `/movies/{movie_id}` | Yes |
| POST | `/movies/{movie_id}/reviews` | No |
| GET | `/watchlists/{watch_list_id}` | No |
| POST | `/watchlists/{watch_list_id}/movies` | Yes |
