# Warehouse Transfers (Django)

Practice debugging stock levels and inter-location transfers.

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

Mutating routes require `Authorization: Bearer secret-token`

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/locations` | No |
| GET | `/locations/{location_id}/stock` | No |
| GET | `/locations/{location_id}/stock/{sku}` | No |
| POST | `/transfers` | Yes |
| GET | `/transfers/{transfer_id}` | No |
