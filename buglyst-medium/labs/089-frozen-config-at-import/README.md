# Frozen Config At Import Time

Test-time env overrides never reach the running config because the snapshot was captured at import.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
