# Subscription Billing (Django)

Practice debugging plans, subscriptions, and idempotent subscribe flows.

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

- Most mutating routes: `Authorization: Bearer secret-token`
- Admin-only routes (`POST /plans`): `Authorization: Bearer admin-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/plans` | No |
| GET | `/plans/{plan_id}` | No |
| POST | `/plans` | Admin |
| PATCH | `/plans/{plan_id}/price` | Admin |
| POST | `/subscriptions` | Yes (`Idempotency-Key` header required) |
| GET | `/subscriptions/{subscription_id}` | No |
| POST | `/subscriptions/{subscription_id}/cancel` | Yes |
