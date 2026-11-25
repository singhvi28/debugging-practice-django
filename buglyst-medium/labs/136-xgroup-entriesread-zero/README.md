# Zero-value entries-read argument omitted from XGROUP tokens

`ENTRIESREAD 0` is dropped from generated command tokens.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
