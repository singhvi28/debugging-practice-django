"""In-memory webhook deduplication with a bounded LRU cache."""

import time
from collections import OrderedDict

# Providers retry within this window; dedupe must retain events at least this long.
PROVIDER_RETRY_WINDOW_SEC = 0.2

MAX_ENTRIES = 2

_seen: OrderedDict[str, float] = OrderedDict()
_processed: list[str] = []


def reset() -> None:
    _seen.clear()
    _processed.clear()


def _evict_if_needed() -> None:
    while len(_seen) > MAX_ENTRIES:
        _seen.popitem(last=False)


def register_event(event_id: str) -> bool:
    """Return True when the event is new, False when it is a duplicate."""
    now = time.time()
    expired = [event_id for event_id, expires_at in _seen.items() if now >= expires_at]
    for event_id in expired:
        del _seen[event_id]

    if event_id in _seen:
        return False

    _seen[event_id] = now + PROVIDER_RETRY_WINDOW_SEC
    _evict_if_needed()
    _processed.append(event_id)
    return True


def processed_events() -> list[str]:
    return list(_processed)
