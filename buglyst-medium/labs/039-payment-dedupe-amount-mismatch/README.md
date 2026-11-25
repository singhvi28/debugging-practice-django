# Payment dedupe ignores amount mismatch

Payment writes honor an `Idempotency-Key` header so retries return the original charge.

## API

- `POST /payments` — create a charge (`amount`, optional `currency`, `Idempotency-Key` header)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
