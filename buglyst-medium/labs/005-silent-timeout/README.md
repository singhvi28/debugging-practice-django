# The Silent Timeout

Outbound dependency calls hang instead of failing fast when the upstream is slow.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
