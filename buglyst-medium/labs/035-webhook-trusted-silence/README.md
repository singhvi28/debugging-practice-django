# The Webhook That Trusted Silence

Inbound webhooks must present a valid `X-Signature` header.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
