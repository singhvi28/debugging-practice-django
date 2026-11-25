"""Record cache with negative caching for misses."""

_store: dict[str, str | None] = {}


def reset() -> None:
    _store.clear()


def is_cached(key: str) -> bool:
    return key in _store


def get_record(key: str) -> str | None:
    return _store.get(key)


def cache_miss(key: str) -> None:
    _store[key] = None


def put_record(key: str, value: str) -> None:
    _store[key] = value
