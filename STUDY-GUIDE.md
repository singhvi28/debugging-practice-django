# Python + Django Study Guide for Debugging Rounds

A practical guide for repository-based debugging assessments when the stack is **Python + Django** (OA-style multi-bug apps, Buglyst-style mini-labs). Goal: read failing tests, find the fault fast, make the smallest correct fix, and leave intentional behavior alone.

Companion materials:

| Doc / area | Use for |
|------------|---------|
| [../CONTEXT.md](../CONTEXT.md) | Reported OA patterns (controller / route / middleware) |
| [01–20](README.md) | Multi-bug Django apps (~6 bugs each; 11–20 slightly harder) |
| [buglyst-medium/](buglyst-medium/) | Single-bug mini-labs |
| [SKILL.md](SKILL.md) | Lab layout conventions for this tree |
| [DJANGO-INTERVIEW-GUIDE.md](DJANGO-INTERVIEW-GUIDE.md) | MVT theory, ORM, DRF, interview answers |
| [../STUDY-GUIDE.md](../STUDY-GUIDE.md) | Parallel FastAPI guide (same bug shapes) |

---

## 1. How debugging rounds work

You usually get an **existing app**, not a blank project:

1. Source (`urls.py`, views, middleware, store/helpers, settings)
2. Docs (README with endpoints / auth)
3. Automated tests that define **correct** behavior

Your job is to make tests pass — not redesign the API or introduce DRF/ORM if the lab is plain Django + in-memory store. Hidden bugs are often ~6 in OA-style repos: **4 view/handler, 1 route, 1 middleware**.

### Workflow (use this every time)

1. **Run the suite** — `pytest -v` (lab `pytest.ini` sets `DJANGO_SETTINGS_MODULE`).
2. **Read failing test names** — they are the spec (`test_search_is_case_insensitive`, `test_…_returns_404`).
3. **Open one failing test** — note method, path, headers, body, expected status/JSON.
4. **Reproduce** — follow that call with `django.test.Client` in your head.
5. **Trace the request path** — middleware → URL resolve → view → store/helper.
6. **Smallest fix** — change the bug site only; re-run; next failure.
7. **Do not “improve”** empty-search, public routes, or status codes the tests already accept.

Time pressure tip: if many authenticated tests return `401`, fix **AuthMiddleware** first — one bug can block half the suite.

---

## 2. Django request path (mental model)

```text
HTTP request
  → Middleware stack (auth, CORS, common)   # may short-circuit
  → URL resolver (urls.py patterns)         # 404 if no match
  → View (+ @require_http_methods)          # 405 if wrong verb
  → Store / helper / (rarely) ORM
  → HttpResponse / JsonResponse
```

When something fails, ask: **did the request reach the view?**

| Symptom | Likely layer |
|---------|----------------|
| All protected routes → `401` even with good token | Middleware never calls `get_response` |
| Public GET unexpectedly `401` | Middleware over-protecting |
| View exists but tests get `404`/`405` | Wrong `path(...)` or `@require_http_methods` |
| `null` body with `200` | View missing not-found `return` |
| Success JSON but later GET misses data | Missing `await` / not persisted |
| `500` on bad input | Validation too late or missing |
| CSRF / 403 on POST in a full Django project | CSRF middleware (these labs use `@csrf_exempt`) |

---

## 3. Django surface you must recognize quickly

### Settings (practice labs)

```python
ROOT_URLCONF = "config.urls"       # or "urls" in mini-labs
APPEND_SLASH = False               # slash-free paths like FastAPI tests
MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "api.middleware.AuthMiddleware",
]
```

`APPEND_SLASH = True` (Django default) can hide or confuse path bugs — these labs turn it off on purpose.

### URLConf

```python
urlpatterns = [
    path("movies", views.movies_collection),           # GET + POST in one view
    path("movies/<str:movie_id>", views.get_movie),
    path("film/<str:movie_id>", views.delete_movie),   # BUG: should be movies/...
    path("orders/<str:order_id>/status", views.update_order_status),
]
```

**One path → one view.** You cannot register GET and POST as two separate `path("movies", ...)` entries. Combine with `@require_http_methods(["GET", "POST"])`.

### Views

```python
@csrf_exempt
@require_http_methods(["GET", "POST"])
def movies_collection(request):
    if request.method == "GET":
        ...
    body = parse_json(request)
    ...
    return JsonResponse(movie, status=201)

@require_http_methods(["GET"])
def get_movie(request, movie_id: str):
    movie = store.get_movie(movie_id)
    # BUG: return JsonResponse(movie, safe=False)  # null + 200
    if movie is None:
        return JsonResponse({"detail": "Movie not found"}, status=404)
    return JsonResponse(movie)
```

### Request data

| Source | Typical use |
|--------|-------------|
| Path converter `<str:movie_id>` | Resource id |
| `request.GET.get("search")` | Query string |
| `json.loads(request.body)` / `parse_json` | JSON body |
| `request.headers.get("Authorization")` | Auth (often middleware) |
| `request.method` | Branch inside combined views |

### Responses

```python
return JsonResponse({"detail": "Unauthorized"}, status=401)
return JsonResponse(items, safe=False)          # list body
return JsonResponse(None, safe=False)           # buggy null 200
return HttpResponse(status=204)                 # delete success
```

**Critical:** building a `JsonResponse(...)` **without `return`** does nothing — execution continues (classic “error then success” bug).

```python
# BUG
if movie is None:
    JsonResponse({"detail": "Movie not found"}, status=404)

# FIX
if movie is None:
    return JsonResponse({"detail": "Movie not found"}, status=404)
```

---

## 4. View / handler bugs (highest volume)

Same shapes as FastAPI controllers — look in `views.py` and `store.py`.

### Case-insensitive / partial search

```python
# BUG
[m for m in movies if m["title"] == search]
# FIX
[m for m in movies if search.lower() in m["title"].lower()]
```

Preserve: no `search` → return all.

### Missing record → 404

```python
if movie is None:
    return JsonResponse({"detail": "Movie not found"}, status=404)
```

### Wrong status on create

`POST` create often expects **`201`**: `return JsonResponse(obj, status=201)`.

### Duplicates / conflicts → `409`

Check before mutate; sold-out / duplicate enrollment usually `409`, bad input `400`.

### Wrong delete predicate

```python
# BUG — keeps the target
items = [i for i in items if i["id"] == target_id]
# FIX
items = [i for i in items if i["id"] != target_id]
```

Or “delete everything except target” when building a new dict of keys.

### Missing `await`

```python
# BUG
store.save_task(project_id, title)   # async — never awaited
return JsonResponse({"id": "t-temp", ...}, status=201)

# FIX
task = await store.save_task(project_id, title)
return JsonResponse(task, status=201)
```

View must be `async def` if it awaits. Tests fail on persistence / id mismatch on follow-up GET.

### Validation too late

Empty title, `quantity <= 0`, negative stock → **`400`** before write.

---

## 5. Routing bugs (`urls.py` + method decorators)

| Bug | Example | Fix |
|-----|---------|-----|
| Wrong path segment | `path("film/<str:id>", ...)` | `movies/<str:id>` |
| Singular vs plural | `.../ingredient` | `.../ingredients` |
| Extra segment | `posts/remove/<id>` | `posts/<id>` |
| Wrong HTTP method | `@require_http_methods(["PUT"])` | `["PATCH"]` (tests call PATCH) |
| Missing include | `config/urls.py` never includes `api.urls` | `path("", include("api.urls"))` |

Django returns **`405`** when the path matches but the method decorator rejects the verb — useful signal: path is right, method is wrong.

Trailing-slash confusion: with `APPEND_SLASH = False`, `/movies/` ≠ `/movies`. Trust the tests’ paths.

---

## 6. Middleware bugs

Typical Bearer middleware in these labs:

```python
class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ...
        if not needs_auth:
            return self.get_response(request)
        ...
        if token != VALID_TOKEN:
            return JsonResponse({"detail": "Unauthorized"}, status=401)
        # BUG: return JsonResponse(..., status=401)
        return self.get_response(request)   # FIX
```

Checklist:

- Reject paths return a response immediately.
- Accept path **must** `return self.get_response(request)`.
- Prefix rules match tests (`POST`/`DELETE` on `/movies`, `/cart`, …).
- Exempt public POSTs (e.g. reviews/comments) explicitly.
- Over-protect bug: force `401` on `GET /projects` or `GET /tracks` — remove that branch.

Middleware order in `settings.MIDDLEWARE`: top runs first on the way in. Auth that never continues looks like “every write is unauthorized.”

### CORS / OPTIONS mini-labs

Preflight often short-circuits with `HttpResponse(status=204)` then sets `Access-Control-*` headers. Bugs: wrong origin regex, missing `Expose-Headers` on preflight only, etc. Keep the bug in the helper/middleware; don’t “fix” by switching to Django’s CORS package mid-round.

---

## 7. HTTP semantics cheat sheet

Match the **project’s tests**, not your preferred REST style.

| Code | Typical meaning in these labs |
|------|-------------------------------|
| `200` | OK read / OK update |
| `201` | Created |
| `204` | Deleted / no body |
| `400` | Bad input |
| `401` | Missing/invalid auth |
| `404` | Missing resource |
| `405` | Method not allowed (decorator / verb) |
| `409` | Conflict (duplicate, sold out) |
| `500` | Unhandled exception |

Error body here is usually `{"detail": "..."}`.

---

## 8. Python + Django pitfalls

| Pitfall | What you see |
|---------|----------------|
| `JsonResponse` without `return` | Wrong status / logic continues |
| `JsonResponse(list)` without `safe=False` | TypeError / 500 |
| Missing `await` on async store | Create “works”, GET empty |
| Two `path()` on same route | Only one view wins / setup confusion |
| `APPEND_SLASH` vs test paths | Mystery 404s |
| CSRF enabled + no exempt | 403 on POST |
| `request.headers` case-insensitive | Hides a “lowercase header dict” bug — feed helpers a plain `dict` if that’s the plant |
| TestClient `params=` | Ignored — use `data=` / `client.get(path, {"q": "x"})` |
| Truthiness of `0` / `""` / `False` | Filters swallow valid falsy values |
| Inverted list filters | Wrong delete / wrong keep |
| Shared module state without `reset()` | Order-dependent flakes |

These labs are mostly **in-memory stores**, not ORM. Don’t waste time on migrations unless the lab is explicitly about migrate/version helpers.

---

## 9. pytest-django + Client (how the oracle works)

```python
import json
import pytest
from django.test import Client

from api import store

AUTH = {"Authorization": "Bearer secret-token"}

@pytest.fixture()
def client():
    store.reset()
    return Client()

def test_create(client):
    r = client.post(
        "/movies",
        data=json.dumps({"title": "Dune", "year": 2021}),
        content_type="application/json",
        headers=AUTH,
    )
    assert r.status_code == 201
    assert r.json()["title"] == "Dune"
```

Skills:

- `client.get/post/put/patch/delete(...)`
- JSON: `data=json.dumps(...)`, `content_type="application/json"`
- Query: `client.get("/movies", {"search": "dark"})`
- `response.status_code`, `response.json()`, `response.headers`
- `pytest.ini`: `DJANGO_SETTINGS_MODULE = config.settings` (or `settings`)

Mini-labs under `buglyst-medium/labs/` use a flat `settings.py` + `urls.py` + `views.py` — same Client patterns.

---

## 10. Timed drill plan

### Warm-up

One [buglyst-medium](buglyst-medium/) lab: confirm fail → fix → green with Django Client.

### Core OA drill

For each of `01-movie-catalog` … `10-order-service`:

1. Time box ~25–40 minutes.
2. Categorize failures: auth wall / search / 404 / route `404`/`405`.
3. Fix middleware if writes are all `401`.
4. Fix `urls.py` / `@require_http_methods` if one endpoint is uniquely unreachable.
5. Finish view/store bugs one test at a time.

### Pattern catalog (memorize)

- Search: case + partial; empty search = all
- Get missing → `404` + `detail`
- Create → `201`
- Duplicate / conflict → `409`
- Bad input → `400`
- Delete filter: keep `!=` target
- Missing `return` after error response
- Missing `await` on async write
- Middleware: valid token → `get_response`
- Route: wrong path string or PUT vs PATCH

### Stretch

Buglyst medium: cache, idempotency, CORS, retries — reading unfamiliar helpers under Django views.

---

## 11. FastAPI ↔ Django translation (if you practiced the other stack)

| FastAPI | Django (these labs) |
|---------|---------------------|
| `@app.get/post` | `path` + `@require_http_methods` |
| `HTTPException` | `return JsonResponse(..., status=...)` |
| `call_next(request)` | `self.get_response(request)` |
| `TestClient` + `json=` | `Client` + `json.dumps` + `content_type` |
| `params=` | query dict / `data=` |
| `status_code=201` on decorator | `JsonResponse(..., status=201)` |
| Pydantic body | `parse_json(request)` + manual checks |
| `Response(404)` discarded | `JsonResponse(404)` without `return` |

Bug essence is the same; only the framework glue differs.

---

## 12. What good looks like in the round

- You **follow tests**, not invent DRF/ORM rewrites.
- Diffs are **small and local** (`views.py`, `urls.py`, `middleware.py`, `store.py`).
- You don’t break empty-list / public-browse behavior while fixing search.
- You re-run the full suite before stopping.
- You can explain each fix in one sentence.

### Red flags (avoid)

- Rewriting to DRF “properly” under time pressure
- Editing tests to match buggy code
- Adding Redis/Docker/real DB when the lab is in-memory
- Creating a per-lab `.venv` (disk bloat; use shared env)

---

## 13. Quick reference commands

```bash
# From a lab folder (shared parent .venv preferred)
pytest -v
pytest -v -k search
pytest --tb=short
python manage.py runserver   # OA-style labs with manage.py
```

Cleanup:

```bash
find . -type d \( -name '.pytest_cache' -o -name '__pycache__' \) -prune -exec rm -rf {} +
find . -name 'db.sqlite3' -delete
```

---

## 14. Link back to practice

1. Skim [../CONTEXT.md](../CONTEXT.md) once (OA pattern list).
2. Grind [01–10](README.md) until the six-bug shape feels automatic in Django, then [11–20](README.md) for harder variants.
3. Use [buglyst-medium/](buglyst-medium/) for single-issue speed.
4. Cross-train with [../STUDY-GUIDE.md](../STUDY-GUIDE.md) if the invite lets you pick FastAPI.

Debugging rounds reward **navigation and pattern recognition**. Django knowledge matters so you can read middleware, URLConf, and views without hesitation — then let the tests define “correct.”
