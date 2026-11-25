# Pagination skips rows on timestamp ties

Activity feeds lose rows when several events share the same `updated_at` timestamp.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
