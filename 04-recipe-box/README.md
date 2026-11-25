# Recipe Box (Django)

Practice debugging a small recipe box API with recipes and ingredients.

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
| GET | `/recipes?search=` | No |
| GET | `/recipes/{recipe_id}` | No |
| POST | `/recipes` | Yes |
| GET | `/recipes/{recipe_id}/ingredients` | No |
| POST | `/recipes/{recipe_id}/ingredients` | Yes |
| DELETE | `/recipes/{recipe_id}/ingredients/{ingredient_id}` | Yes |
