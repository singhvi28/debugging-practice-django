# The Timezone Trap

Daily reports bucket events on the wrong calendar day around midnight UTC.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
