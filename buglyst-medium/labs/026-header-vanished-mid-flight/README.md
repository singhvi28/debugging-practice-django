# The Header That Vanished Mid-Flight

Authenticated upstream calls return 401 even though the client set Authorization.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
