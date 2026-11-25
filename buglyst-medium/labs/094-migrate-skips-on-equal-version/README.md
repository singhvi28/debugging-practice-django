# Migrate Skips On Equal Version

Schema migrations stop applying even though the database never received the change.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
