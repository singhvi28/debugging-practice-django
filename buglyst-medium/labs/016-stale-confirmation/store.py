"""In-memory item store with read-through cache."""

_store: dict[str, str] = {"widget": "v1"}
_cache: dict[str, str] = {}


def reset() -> None:
    global _store, _cache
    _store = {"widget": "v1"}
    _cache.clear()


def read_item(item_id: str) -> str:
    if item_id in _cache:
        return _cache[item_id]
    value = _store[item_id]
    _cache[item_id] = value
    return value


def write_item(item_id: str, value: str) -> str:
    _store[item_id] = value
    return value
