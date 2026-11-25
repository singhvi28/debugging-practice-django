# Lowercase header lookup

Authenticated requests fail when the gateway normalizes header names differently than the caller.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
