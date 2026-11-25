# N+1 that silently drops rows

Order listings come back short because the per-row user lookup never matches.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
