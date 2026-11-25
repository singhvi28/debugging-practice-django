# Token bucket refills on every request

Each call resets the bucket to capacity, so the limiter never throttles.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
