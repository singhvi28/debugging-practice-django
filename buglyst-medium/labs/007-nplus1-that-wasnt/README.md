# The N+1 That Wasn't

Listing orders is slow even though the database query count looks fine.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
