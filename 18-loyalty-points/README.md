# Loyalty Points (Django)

Practice debugging account balances, earn/redeem flows, and ledger entries.

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

- `GET /accounts/{account_id}/balance` — requires `Authorization: Bearer secret-token`
- `POST /accounts/{account_id}/earn` — requires auth
- `POST /accounts/{account_id}/redeem` — requires auth

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/accounts` | No |
| GET | `/accounts/{account_id}` | No |
| GET | `/accounts/{account_id}/balance` | Yes |
| POST | `/accounts/{account_id}/earn` | Yes |
| POST | `/accounts/{account_id}/redeem` | Yes |
| GET | `/accounts/{account_id}/ledger` | No |
