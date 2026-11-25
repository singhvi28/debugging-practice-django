# Cache Stampede

Concurrent requests after cache expiry hammer the backend instead of coalescing.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
