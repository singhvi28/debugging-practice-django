# Bookstore (Django)

Practice debugging a small bookstore API with books and shopping carts.

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
| GET | `/books?search=` | No |
| GET | `/books/{book_id}` | No |
| POST | `/books` | Yes |
| DELETE | `/books/{book_id}` | Yes |
| GET | `/cart/{cart_id}` | No |
| POST | `/cart/{cart_id}/items` | Yes |
| DELETE | `/cart/{cart_id}/items/{book_id}` | Yes |
