# Dotenv Empty String Truthy

An unset env var with an empty default still turns a maintenance flag on.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
