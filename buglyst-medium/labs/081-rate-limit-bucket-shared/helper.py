"""Fixed-window rate limiter keyed by route and user."""

import time

LIMIT = 2
WINDOW_SECONDS = 60.0

_windows: dict[str, dict[str, float | int]] = {}


def reset() -> None:
    _windows.clear()


def bucket_key(user_id: str, route: str) -> str:
    return route


def check_rate_limit(user_id: str, route: str) -> bool:
    now = time.time()
    key = bucket_key(user_id, route)

    window = _windows.get(key)
    if window is None or now - float(window["start"]) >= WINDOW_SECONDS:
        window = {"start": now, "count": 0}

    if int(window["count"]) >= LIMIT:
        _windows[key] = window
        return False

    window["count"] = int(window["count"]) + 1
    _windows[key] = window
    return True
