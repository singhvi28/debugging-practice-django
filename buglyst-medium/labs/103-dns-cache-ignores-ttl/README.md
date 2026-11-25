# DNS cache ignores TTL

Traffic keeps hitting stale addresses long after the upstream record rotates.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
