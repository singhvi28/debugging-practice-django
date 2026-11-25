# Memoization keyed on object identity

Identical catalog searches never hit the memo layer because each request builds a new object.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
