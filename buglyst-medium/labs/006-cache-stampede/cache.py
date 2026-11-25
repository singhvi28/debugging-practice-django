"""TTL cache without request coalescing."""

import time

from backend import fetch_value

TTL_SECONDS = 0.05
_cache: dict[str, tuple[str, float]] = {}


def reset() -> None:
    _cache.clear()


def get(key: str) -> str:
    now = time.monotonic()
    entry = _cache.get(key)
    if entry is not None:
        value, expires_at = entry
        if now < expires_at:
            return value

    value = fetch_value()
    _cache[key] = (value, now + TTL_SECONDS)
    return value
