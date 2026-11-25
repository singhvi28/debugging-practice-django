# The Query That Loaded the World

Orders list endpoint returns every tenant's rows and times out under load.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
