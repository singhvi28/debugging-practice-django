"""In-memory event bus with webhook delivery."""

from collections.abc import Callable

Listener = Callable[[dict], None]

_listeners: list[Listener] = []
_webhook_log: list[dict] = []


def reset() -> None:
    _listeners.clear()
    _webhook_log.clear()
    register_listener(_record_webhook)


def _record_webhook(event: dict) -> None:
    _webhook_log.append(event)


def register_listener(listener: Listener) -> None:
    _listeners.append(listener)


def reconnect() -> None:
    register_listener(_record_webhook)


def emit_event(event: dict) -> int:
    for listener in list(_listeners):
        listener(event)
    return len(_listeners)


def webhook_deliveries() -> list[dict]:
    return list(_webhook_log)
