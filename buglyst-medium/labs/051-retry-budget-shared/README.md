# Retry Budget Shared Across Callers

A shared retry budget limits how many upstream attempts the service may make.

## API

- `POST /call/{caller_id}?failures_before_success=0` — run a flaky upstream call
- `GET /budget` — remaining retry budget slots


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
