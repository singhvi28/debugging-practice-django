"""Concurrency permit pool."""

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

_max_permits = 1
_available = 1


def reset(max_permits: int = 1) -> None:
    global _max_permits, _available
    _max_permits = max_permits
    _available = max_permits


def available_permits() -> int:
    return _available


def acquire() -> None:
    global _available
    if _available <= 0:
        raise RuntimeError("no permits available")
    _available -= 1


def release() -> None:
    global _available
    _available += 1


def with_lock(fn: Callable[[], T]) -> T:
    acquire()
    try:
        result = fn()
        release()
        return result
    finally:
        release()
