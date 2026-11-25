# AccessDenied at 3AM

After credential rotation, protected calls start failing with access denied.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
