# Circuit Half-Open Floods Requests

A circuit breaker protects a flaky downstream service.

## API

- `POST /proxy` — forward a request when the circuit allows it
- `POST /proxy/success` — forward and record downstream success
- `POST /admin/half-open` — move the circuit to half-open (test helper)
- `GET /circuit` — current breaker state
- `GET /_debug/downstream-calls` — downstream call counter (test helper)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
