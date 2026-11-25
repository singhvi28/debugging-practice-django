"""Exclusive resource locks for background jobs."""

_held: set[str] = set()


def reset() -> None:
    _held.clear()


def is_locked(resource: str) -> bool:
    return resource in _held


def run_with_lock(resource: str, should_fail: bool) -> None:
    if resource in _held:
        raise RuntimeError("resource is locked")
    _held.add(resource)
    if should_fail:
        raise ValueError("job failed")
    _held.discard(resource)
