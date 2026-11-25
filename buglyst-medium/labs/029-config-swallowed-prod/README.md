# The Config That Swallowed Prod

Production boots with the dev database URL and debug flags.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
