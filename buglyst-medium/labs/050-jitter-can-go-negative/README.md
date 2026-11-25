# Jitter Can Go Negative

The retry scheduler applies subtractive jitter to backoff delays.

## API

- `POST /jitter` — body: `{ "base_ms": 50, "jitter_ms": 200, "seed": 42 }` returns the jittered delay


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
