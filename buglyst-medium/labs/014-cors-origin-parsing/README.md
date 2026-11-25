# CORS Origin Parsing Bug

Origin validation is too permissive for certain lookalike domains.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
