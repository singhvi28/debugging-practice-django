# Inventory (Django)

Practice debugging a small inventory API with products and stock moves.

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
| GET | `/products?search=` | No |
| GET | `/products/{product_id}` | No |
| POST | `/products` | Yes |
| POST | `/products/{product_id}/stock` | Yes |
| GET | `/products/{product_id}/moves` | No |
| DELETE | `/products/{product_id}` | Yes |
