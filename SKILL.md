---
name: django-debugging-labs
description: >-
  Build and maintain Django debugging practice labs (OA-style multi-bug apps and
  Buglyst-style single-bug mini-labs) with pytest-django as the correctness
  oracle. Use when creating intentional-bug Django repos, porting FastAPI
  Buglyst labs to Django, batching Composer subagents to generate labs, or
  cleaning up lab venvs/caches.
---

# Django Debugging Practice Labs

Conventions learned while building this workspace: OA-style multi-bug Django apps, Buglyst medium mini-labs, FastAPI→Django porting, subagent batching, and disk hygiene.

Parent FastAPI workspace (source patterns / CONTEXT): [`../`](../) — especially [`../CONTEXT.md`](../CONTEXT.md) and [`../SKILL.md`](../SKILL.md).

## Workspace map

| Path | What |
|------|------|
| [`../CONTEXT.md`](../CONTEXT.md) | Amazon OA-style backend debugging patterns (controllers, routes, middleware) |
| [`01-…`–`10-…`](README.md) | Multi-bug Django apps (~6 bugs each: 4 view/handler, 1 route, 1 middleware) |
| [`buglyst-medium/`](buglyst-medium/) | Single-bug mini-labs from [`QUESTIONS.md`](buglyst-medium/QUESTIONS.md) |
| [`.gitignore`](.gitignore) | Excludes `.venv`, `__pycache__`, `.pytest_cache`, `db.sqlite3` |

**Defaults:** no answer keys; pytest asserts correct behavior and fails while the bug is present; in-memory only (no Redis/Docker/real DBs). Prefer sqlite `:memory:` or unused sqlite files over real persistence.

## Stack pins

```text
Django==5.1.4
pytest==8.3.4
pytest-django==4.9.0
```

## Running tests (no per-lab venv)

Prefer one shared environment (parent `../.venv` or this tree’s `.venv`). From a lab folder:

```bash
pytest -v
```

Each lab’s `pytest.ini` sets `DJANGO_SETTINGS_MODULE` and `pythonpath = .`.

### Disk hygiene (critical)

**Never** create a `.venv` inside each lab. Per-lab venvs balloon disk usage; source alone is small.

Cleanup if it happens again (run from this folder or the parent workspace):

```bash
find . -type d -name '.venv' ! -path './.venv' ! -path './.venv/*' -prune -exec rm -rf {} +
find . -type d \( -name '__pycache__' -o -name '.pytest_cache' \) -prune -exec rm -rf {} +
find . -type f -name 'db.sqlite3' -delete
```

## Pattern A — OA multi-bug app (6 bugs)

Layout:

```text
NN-domain/
  README.md              # run instructions; NO bug list
  requirements.txt
  manage.py
  pytest.ini             # DJANGO_SETTINGS_MODULE = config.settings
  config/
    settings.py          # APPEND_SLASH = False; AuthMiddleware registered
    urls.py              # path("", include("api.urls"))
  api/
    store.py             # in-memory + reset()
    middleware.py        # exactly 1 middleware bug + parse_json helper
    views.py             # controller bugs
    urls.py              # route bug lives here (wrong path or method)
  tests/
    conftest.py          # store.reset(); django.test.Client()
    test_api.py
```

Bug mix (reported OA pattern):

1. **View/handler ×4** — e.g. case-sensitive search, missing `404`, no duplicate `409`, missing `return` after error, missing `await`, wrong delete predicate, late validation → `500`, wrong status (`200` vs `201`/`204`)
2. **Route ×1** — wrong path/method (e.g. `/film/{id}` instead of `/movies/{id}`, `PUT` instead of `PATCH`)
3. **Middleware ×1** — valid token never calls `get_response`, auth on public route, or missing on protected route

### Django-specific rules

- **`APPEND_SLASH = False`** — paths match FastAPI (no trailing slash).
- **No CSRF middleware** on practice APIs; use `@csrf_exempt` on mutating views.
- **One URL path → one view.** Combine GET+POST collections into one view with `@require_http_methods(["GET", "POST"])` (Django cannot register two views on the same path).
- **JSON:** `JsonResponse(data)`; lists need `safe=False`. Missing-record bug often returns `JsonResponse(None, safe=False)` (200 + null) instead of 404. Empty success: `HttpResponse(status=204)`.
- **Auth header:** `Authorization: Bearer secret-token`. Error body shape: `{"detail": "..."}`.
- **Tests:** `django.test.Client`; bodies via `json.dumps(...)` + `content_type="application/json"`; headers via `headers={"Authorization": "Bearer secret-token"}`. Query params: `client.get("/path", {"search": "x"})` (Django’s `data=`), not httpx-style `params=`.

### Route-bug safety

Prefer wrong path string or wrong HTTP method (`@require_http_methods(["PUT"])` while tests call `PATCH`). Avoid path-param / signature mismatches that crash URL resolution at import/setup.

### Async bug safety

Missing-`await` bugs must still return a JSON-serializable response. Do not return an unawaited coroutine from a view — call the async store without `await`, then return a placeholder body so tests fail on persistence, not on encoder crashes.

### Middleware bug pattern

After a valid Bearer token check, the buggy middleware returns `401` instead of `return self.get_response(request)`. Over-protect bugs force auth on a public GET (e.g. `GET /projects` or `GET /tracks`).

## Pattern B — Buglyst mini-lab (1 bug)

Compact flat layout (no `manage.py` / `config/` package required):

```text
buglyst-medium/labs/NNN-kebab-slug/
  README.md              # title + how to run; no spoilers
  requirements.txt
  pytest.ini             # DJANGO_SETTINGS_MODULE = settings
  settings.py            # minimal; APPEND_SLASH = False; sqlite :memory:
  urls.py
  views.py               # thin Django surface (replaces FastAPI app.py)
  helper.py              # optional 2nd file (store/cache/retry/…)
  tests/
    conftest.py          # optional; Client + helper reset()
    test_app.py
```

### Minimal `settings.py`

```python
SECRET_KEY = "django-insecure-debugging-practice-only"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "urls"
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
APPEND_SLASH = False
USE_TZ = True
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
INSTALLED_APPS = ["django.contrib.contenttypes"]
```

Add a custom middleware module to `MIDDLEWARE` when the lab’s bug is CORS / auth / header forwarding.

### Adaptation rule

Preserve the **bug essence** from QUESTIONS.md (or the FastAPI lab). Wrap ops/JS/open-source scenarios as Django views + in-memory helpers:

| Original | Lab shape |
|----------|-----------|
| Cache / TTL / keys | In-memory cache behind GET/PUT |
| Auth / CORS / status | Real routes + middleware |
| Retry / timeout / batch | Helpers + `POST /jobs` or unit tests |
| Races / locks | Shared state + concurrent Client/threads |
| Config / env / CWD / argv | Loader used at startup; tests set env/cwd |
| Open-source helpers | Pure Python + thin Django view wrapper |

When porting from FastAPI: helper modules with pure logic are often copyable verbatim; only `app.py` becomes `views.py` + `urls.py`. Watch Django footguns:

- `request.headers` is case-insensitive — if the bug is lowercase dict lookup, feed the helper a plain `dict`, not Django’s headers object.
- TestClient query strings use `data=` / positional dict, not `params=`.
- OPTIONS/CORS labs need middleware that short-circuits preflight (`HttpResponse(status=204)`) and sets headers.

### Race / concurrency labs

Widen the race window (e.g. short `time.sleep` between check and write) so concurrent tests **reliably fail** with the bug. Flaky “sometimes green” labs are broken.

### Smoke verify checklist

After generating many labs:

1. Every lab folder exists (match QUESTIONS.md / README index)
2. App imports cleanly (`collected N` > 0)
3. Suite has **≥1 failed** test (not all-green, not import ERROR)
4. Fix outliers: missing labs, all-pass buggy code, skipped-only suites

## Generating labs with Composer subagents

For large batches (40–65 labs):

1. Write README index first (folder names locked)
2. Create one reference lab (e.g. `004-…`) and point agents at it
3. Launch parallel `Task` agents with `model: composer-2.5`, ~8–11 labs each
4. Each prompt must include: Django layout rules, exact folder names, “preserve FastAPI bug essence”, “tests assert correct behavior”, “no SOLUTIONS”, “do not create per-lab `.venv` — use shared env + `pytest -v`”
5. Parent smoke-verifies and patches gaps

## QUESTIONS.md formatting

Scraped Buglyst lists arrive as broken field-per-line dumps. Reformat to:

1. Title + intro
2. Summary table (ID | Title | Difficulty | Time) with anchor links
3. `### ID — Title` sections with metadata line + description
4. Inline code for identifiers (`Idempotency-Key`, `JSON.stringify`, etc.)

## Learner workflow (document in READMEs)

1. Read failing test names
2. Reproduce one failure
3. Smallest fix
4. Re-run until green
5. Do not break intentional empty-search / empty-list behavior while fixing matching

## Anti-patterns

- Per-lab virtualenvs
- Answer keys in-repo unless the user asks
- Duplicate `path()` entries for the same URL (combine methods in one view)
- Leaving `APPEND_SLASH = True` when tests expect slash-free FastAPI paths
- Returning unawaited coroutines from views
- Concurrent tests that pass by luck without a forced race window
- Spoilers in lab READMEs
- `# BUG:` / `# Expected:` annotations in lab source (spoils the exercise; bugs must be active code only)
- Real networks, Docker, Redis, or external DBs in these practice labs
- Feeding Django’s case-insensitive headers into a case-sensitive lookup bug (hides the bug)
