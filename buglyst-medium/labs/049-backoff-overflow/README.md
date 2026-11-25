# Backoff Overflow at High Attempts

The retry scheduler computes exponential backoff delays for outbound calls.

## API

- `GET /backoff/{attempt}` — returns the computed delay in milliseconds for the given attempt number


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
