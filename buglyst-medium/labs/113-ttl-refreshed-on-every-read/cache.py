"""In-memory TTL cache for session fragments."""

_now: float = 0.0
_entries: dict[str, dict] = {}


def reset() -> None:
    global _now
    _now = 0.0
    _entries.clear()


def set_clock(value: float) -> None:
    global _now
    _now = value


def clock() -> float:
    return _now


def put(key: str, value: str, ttl_seconds: float) -> None:
    _entries[key] = {
        "value": value,
        "expires_at": _now + ttl_seconds,
        "ttl_seconds": ttl_seconds,
    }


def get(key: str) -> str | None:
    entry = _entries.get(key)
    if entry is None:
        return None
    if _now >= entry["expires_at"]:
        del _entries[key]
        return None
    entry["expires_at"] = _now + entry["ttl_seconds"]
    return entry["value"]
