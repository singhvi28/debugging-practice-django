# Dedupe cache evicts too eagerly

Webhook deliveries are deduplicated in memory so provider retries do not double-process events.

## API

- `POST /webhooks` — accept a webhook (`event_id`, `payload`)
- `GET /_debug/processed` — list processed event ids (testing helper)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
