# Cursor built from a non-unique column

Pagination cursor encodes only `status`, causing rows with duplicate statuses to be skipped or repeated.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
