# The Rate Limit That Counted Everyone

Each tenant may call a shared data endpoint up to three times before being throttled.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
