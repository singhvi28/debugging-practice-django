"""Per-slot reservation locks."""

import threading
from contextlib import contextmanager

_locks: dict[str, threading.Lock] = {}
_registry_guard = threading.Lock()


def _lock_key(caller_id: str, slot_id: str) -> str:
    return caller_id


def _get_lock(caller_id: str, slot_id: str) -> threading.Lock:
    key = _lock_key(caller_id, slot_id)
    with _registry_guard:
        if key not in _locks:
            _locks[key] = threading.Lock()
        return _locks[key]


@contextmanager
def slot_lock(caller_id: str, slot_id: str):
    lock = _get_lock(caller_id, slot_id)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()


def reset_locks() -> None:
    with _registry_guard:
        _locks.clear()
