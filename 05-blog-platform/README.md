# Blog Platform (Django)

Practice debugging a small blog platform API with posts and comments.

## Setup

```bash
# Prefer the shared parent .venv — do not create a per-lab venv
pip install -r requirements.txt
pytest -v
```

## Run locally

```bash
python manage.py runserver
```

## Auth

Protected routes expect:

```text
Authorization: Bearer secret-token
```

## Endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/posts?search=` | No |
| GET | `/posts/{post_id}` | No |
| POST | `/posts` | Yes |
| DELETE | `/posts/{post_id}` | Yes |
| GET | `/posts/{post_id}/comments` | No |
| POST | `/posts/{post_id}/comments` | No |
