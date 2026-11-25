# LRU Evicts the Wrong Tenant Entry

A per-tenant LRU cache keeps hot keys near capacity.

## API

- `PUT /cache/{tenant}/{key}` — store a value
- `GET /cache/{tenant}/{key}` — read a value
- `GET /cache/{tenant}/_keys` — list cached keys for a tenant


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
