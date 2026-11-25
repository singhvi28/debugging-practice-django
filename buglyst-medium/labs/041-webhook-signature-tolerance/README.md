# Webhook signature tolerance too wide

Inbound webhooks include a timestamped HMAC signature. Signatures older than a few minutes must be rejected.

## API

- `POST /webhooks` — process a signed webhook (`X-Signature-Timestamp`, `X-Signature`)
- `GET /_debug/processed` — list processed event ids (testing helper)


## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
