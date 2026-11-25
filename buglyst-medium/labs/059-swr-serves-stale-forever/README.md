# Stale-While-Revalidate Serves Stale Forever

A cache serves stale entries while revalidating in the background.

## API

- `GET /cache/{key}` — read a cached value
- `GET /_debug/fetch-count/{key}` — how many times the fetcher ran (test helper)
- `POST /_debug/wait-stale` — wait until entries become stale (test helper)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
