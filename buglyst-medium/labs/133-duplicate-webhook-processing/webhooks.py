"""Webhook dispatch with pluggable listeners."""

from collections.abc import Callable

_listeners: list[Callable[[dict], None]] = []
_processed: list[str] = []


def reset() -> None:
    _listeners.clear()
    _processed.clear()


def register_listener(handler: Callable[[dict], None]) -> None:
    _listeners.append(handler)


def record_processed(event_id: str) -> None:
    _processed.append(event_id)


def dispatch(event: dict) -> int:
    for handler in _listeners:
        handler(event)
    return len(_listeners)


def processed_events() -> list[str]:
    return list(_processed)
