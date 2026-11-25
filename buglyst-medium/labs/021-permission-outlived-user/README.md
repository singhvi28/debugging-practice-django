# The Permission That Outlived the User

Security revokes a contractor account, but the API still accepts destructive calls from that user.

## API

- `POST /revoke` — revoke a user (`{"user_id": "contractor-7"}`)
- `DELETE /resources/{resource_id}` — delete a resource (header `X-User-Id`)

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
