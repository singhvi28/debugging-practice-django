# The Dashboard That Averaged Averages

On-call swears p95 is fine. Customers still time out.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
