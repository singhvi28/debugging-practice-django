# The Flaky Retry

Retry logic keeps hammering a failing upstream instead of giving up.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
