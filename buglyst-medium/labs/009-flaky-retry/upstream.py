"""Simulated upstream that always returns 503."""

_attempts = 0


class ServiceUnavailable(Exception):
    pass


def reset() -> None:
    global _attempts
    _attempts = 0


def call_upstream() -> dict:
    global _attempts
    _attempts += 1
    raise ServiceUnavailable("upstream unavailable")


def get_attempts() -> int:
    return _attempts
