# Order Service (Django)

Practice debugging a small order service API with products and order management.

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
| POST | `/orders` | Yes |
| GET | `/orders/{order_id}` | No |
| PATCH | `/orders/{order_id}/status` | Yes |
| DELETE | `/orders/{order_id}` | Yes |
