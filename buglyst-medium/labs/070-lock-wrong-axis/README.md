# Lock Around the Wrong Axis

Reservations for distinct slots owned by the same caller serialize unnecessarily.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
