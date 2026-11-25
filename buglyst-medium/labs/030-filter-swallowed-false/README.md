# The Filter That Swallowed False

`?includeDeleted=false` still returns soft-deleted rows.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
