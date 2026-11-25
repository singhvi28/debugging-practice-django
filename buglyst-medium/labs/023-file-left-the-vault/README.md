# The File That Left the Vault

A document download endpoint serves more than the vault folder.

## API

- `GET /files?path=` — read a file from the vault by relative path

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
