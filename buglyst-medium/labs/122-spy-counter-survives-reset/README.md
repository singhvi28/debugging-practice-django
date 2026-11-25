# Spy Counter Survives Reset

After resetting the spy between tests, the invocation count no longer matches the call log.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
