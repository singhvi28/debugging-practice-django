# Loop Mutates the Source Array

Some queued jobs never run after another job is skipped.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
