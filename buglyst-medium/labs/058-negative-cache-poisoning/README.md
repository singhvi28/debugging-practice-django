# Negative Cache Poisoning

A read-through cache accelerates record lookups.

## API

- `GET /records/{key}` — fetch a record (cached on success)
- `POST /records/{key}` — create a record in the backing store


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
