# Django Debugging Practice

Twenty-five small Django apps with intentional bugs. Each repo has a pytest suite that defines correct API behavior — fix the code until the tests pass.

Mirrors the FastAPI labs in the parent folder and the patterns in [CONTEXT.md](../CONTEXT.md) (controller, routing, and middleware faults).

Study guide for debugging rounds: [STUDY-GUIDE.md](STUDY-GUIDE.md).

Django development + interview guide (MVT, ORM, DRF): [DJANGO-INTERVIEW-GUIDE.md](DJANGO-INTERVIEW-GUIDE.md).

Canonical Django directory structure + architecture guide: [DJANGO-DIRECTORY-STRUCTURE.md](DJANGO-DIRECTORY-STRUCTURE.md).

## Repos

| # | Folder | Domain | Difficulty |
|---|--------|--------|--------|
| 01 | [01-movie-catalog](01-movie-catalog) | Movies, reviews, watchlists | Very Easy |
| 02 | [02-bookstore](02-bookstore) | Books and shopping cart | Very Easy |
| 03 | [03-task-manager](03-task-manager) | Projects and tasks | Very Easy |
| 04 | [04-recipe-box](04-recipe-box) | Recipes and ingredients | Very Easy |
| 05 | [05-blog-platform](05-blog-platform) | Posts and comments | Very Easy |
| 06 | [06-inventory](06-inventory) | Products and stock moves | Very Easy |
| 07 | [07-music-playlists](07-music-playlists) | Tracks and playlists | Very Easy |
| 08 | [08-event-tickets](08-event-tickets) | Events and tickets | Very Easy |
| 09 | [09-course-enroll](09-course-enroll) | Courses and enrollments | Very Easy |
| 10 | [10-order-service](10-order-service) | Products and orders | Very Easy |
| 11 | [11-library-loans](11-library-loans) | Books and loans | Easy |
| 12 | [12-hotel-reservations](12-hotel-reservations) | Rooms and bookings | Easy |
| 13 | [13-expense-reports](13-expense-reports) | Reports and line items | Easy |
| 14 | [14-forum-threads](14-forum-threads) | Threads and replies | Easy |
| 15 | [15-file-metadata](15-file-metadata) | Files and tags | Easy |
| 16 | [16-subscription-billing](16-subscription-billing) | Plans and subscriptions | Easy |
| 17 | [17-appointment-scheduler](17-appointment-scheduler) | Providers and appointments | Easy |
| 18 | [18-loyalty-points](18-loyalty-points) | Accounts and ledger | Easy |
| 19 | [19-notification-inbox](19-notification-inbox) | Notifications | Easy |
| 20 | [20-warehouse-transfers](20-warehouse-transfers) | Locations and transfers | Easy |
| 21 | [21-marketplace-checkout](21-marketplace-checkout) | Cart, inventory, and checkout | Medium-Hard |
| 22 | [22-project-board](22-project-board) | Projects, tasks, and pagination | Medium-Hard |
| 23 | [23-delivery-tracking](23-delivery-tracking) | Shipment state and webhooks | Medium-Hard |
| 24 | [24-media-processing](24-media-processing) | Media jobs and signed URLs | Medium-Hard |
| 25 | [25-expense-approvals](25-expense-approvals) | Expense approval workflows | Medium-Hard |

Each repo plants **6 bugs**: typically 4 in views/handlers, 1 in routing (`urls.py`), and 1 in middleware. Repos **11–20** are slightly harder; repos **21–25** add stronger cross-resource invariants, state machines, idempotency, pagination, and concurrency traps.

Single-bug Buglyst medium mini-labs: [buglyst-medium/](buglyst-medium/).

## How to practice

From the parent workspace (shared `.venv` preferred — do **not** create a venv per lab):

```bash
cd debugging-practice-django/01-movie-catalog
pip install -r requirements.txt   # once, into the shared env
pytest -v
```

Read failing test names, reproduce one failure, make the smallest fix, then re-run the suite. Repeat until green.

Optional: run the API locally with `python manage.py runserver`.

## Cleanup generated files

Preview and remove Python/test caches from the workspace:

```bash
./scripts/cleanup_generated.sh
./scripts/cleanup_generated.sh --apply
```

## Tips

- Prefer reading failing tests before rewriting large chunks of code.
- Check URL patterns, HTTP methods, status codes, and middleware order.
- Watch for missing `return` after error responses.
- Empty search / list behavior is usually intentional — do not break it while fixing case or partial matching.
- Auth header for protected routes: `Authorization: Bearer secret-token` (some labs also use `admin-token`)
