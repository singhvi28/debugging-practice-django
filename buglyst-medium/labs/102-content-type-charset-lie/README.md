# Content-Type charset lie

Partners send Latin-1 payloads but the decoder always assumes UTF-8.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
