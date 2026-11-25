"""Stale-while-revalidate cache."""

import time

FRESH_TTL_SEC = 0.05
STALE_TTL_SEC = 0.5

_entries: dict[str, dict] = {}
_fetch_counts: dict[str, int] = {}


def reset() -> None:
    _entries.clear()
    _fetch_counts.clear()


def fetch_count(key: str) -> int:
    return _fetch_counts.get(key, 0)


def _fetch(key: str) -> str:
    _fetch_counts[key] = _fetch_counts.get(key, 0) + 1
    return f"fresh-{key}-v{_fetch_counts[key]}"


class CacheEntry:
    def __init__(self, value: str, fetched_at: float):
        self.value = value
        self.fetched_at = fetched_at

    def is_fresh(self) -> bool:
        return time.time() - self.fetched_at < FRESH_TTL_SEC

    def is_stale_but_servable(self) -> bool:
        age = time.time() - self.fetched_at
        return FRESH_TTL_SEC <= age < FRESH_TTL_SEC + STALE_TTL_SEC


def get_value(key: str) -> str:
    entry = _entries.get(key)
    if entry is None:
        value = _fetch(key)
        _entries[key] = CacheEntry(value, time.time())
        return value
    if entry.is_fresh():
        return entry.value
    if entry.is_stale_but_servable():
        return entry.value
    value = _fetch(key)
    _entries[key] = CacheEntry(value, time.time())
    return value
