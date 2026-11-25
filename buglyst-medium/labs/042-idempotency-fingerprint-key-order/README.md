# Idempotency fingerprint key-order sensitive

Write operations dedupe identical request bodies using a content fingerprint.

## API

- `POST /operations` — create an operation (`account`, `amount`, optional `currency`)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
