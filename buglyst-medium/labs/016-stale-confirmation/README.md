# The Stale Confirmation

Updates succeed in storage but the API confirmation echoes an old value.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
