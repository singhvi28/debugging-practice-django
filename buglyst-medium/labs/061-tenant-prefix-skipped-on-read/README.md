# Tenant Prefix Skipped on Read

A multi-tenant key-value store namespaces entries per tenant.

## API

- `PUT /kv/{tenant}/{key}` — write a value
- `GET /kv/{tenant}/{key}` — read a value

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
