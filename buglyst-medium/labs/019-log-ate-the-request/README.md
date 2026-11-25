# The Log That Ate the Request

Debug logging may be capturing more of the upload payload than intended.

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
