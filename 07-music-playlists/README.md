# Music Playlists (Django)

Practice debugging a small music API with tracks and playlists.

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
| GET | `/tracks?search=` | No |
| GET | `/tracks/{track_id}` | No |
| POST | `/tracks` | Yes |
| GET | `/playlists/{playlist_id}` | No |
| POST | `/playlists/{playlist_id}/tracks` | Yes |
| DELETE | `/playlists/{playlist_id}/tracks/{track_id}` | Yes |
