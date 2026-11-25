# Preflight omits Access-Control-Expose-Headers

Custom response headers are invisible to cross-origin callers because the preflight never declares them.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
