# Task Manager (Django)

Practice debugging a small task manager API with projects and tasks.

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
| GET | `/projects?search=` | No |
| GET | `/projects/{project_id}` | No |
| POST | `/projects` | Yes |
| GET | `/projects/{project_id}/tasks` | No |
| POST | `/projects/{project_id}/tasks` | Yes |
| PATCH | `/tasks/{task_id}` | Yes |
| DELETE | `/tasks/{task_id}` | Yes |
