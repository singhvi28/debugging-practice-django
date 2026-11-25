# Course Enrollment (Django)

Practice debugging a small course enrollment API with student registrations.

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
| GET | `/courses?search=` | No |
| GET | `/courses/{course_id}` | No |
| POST | `/courses` | Yes |
| POST | `/courses/{course_id}/enrollments` | Yes |
| GET | `/courses/{course_id}/enrollments` | No |
| DELETE | `/enrollments/{enrollment_id}` | Yes |
