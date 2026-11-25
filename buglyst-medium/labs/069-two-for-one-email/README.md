# Two For One Email

A registration endpoint creates user accounts by email address.

## API

- `POST /register` — body: `{ "email": "user@example.com" }`
- `GET /users/count` — total registered users

## Run

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

Fix the code until tests pass.
