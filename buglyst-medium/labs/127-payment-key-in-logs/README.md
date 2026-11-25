# The Payment Key That Ended Up In The Logs

Failed charges leak sensitive credentials in error responses.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
