# Rate-limit bucket shared across users

The rate-limit key omits the user id, so every caller shares one bucket per route.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
