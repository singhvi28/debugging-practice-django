"""Cursor pagination over a static task list."""

import base64
import json

TASKS: list[dict[str, str]] = [
    {"id": "t1", "title": "Alpha", "status": "open"},
    {"id": "t2", "title": "Beta", "status": "open"},
    {"id": "t3", "title": "Gamma", "status": "open"},
    {"id": "t4", "title": "Delta", "status": "closed"},
    {"id": "t5", "title": "Epsilon", "status": "closed"},
    {"id": "t6", "title": "Zeta", "status": "closed"},
]


def encode_cursor(task: dict[str, str]) -> str:
    payload = {"status": task["status"]}
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode()


def decode_cursor(cursor: str) -> dict[str, str]:
    raw = base64.urlsafe_b64decode(cursor.encode())
    return json.loads(raw)


def paginate(cursor: str | None, limit: int) -> tuple[list[dict[str, str]], str | None]:
    items = TASKS
    if cursor:
        marker = decode_cursor(cursor)
        items = [task for task in TASKS if task["status"] > marker["status"]]

    page = items[:limit]
    next_cursor = encode_cursor(page[-1]) if len(items) > limit else None
    return page, next_cursor
