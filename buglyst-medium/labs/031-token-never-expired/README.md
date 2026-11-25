# The Token That Never Expired

Bearer sessions gate access to a profile endpoint. Each session carries an `expiresAt` timestamp.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
