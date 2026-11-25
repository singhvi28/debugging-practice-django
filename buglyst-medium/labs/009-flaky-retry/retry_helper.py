"""Retry helper for upstream calls."""

from upstream import ServiceUnavailable

MAX_ATTEMPTS = 3


def call_with_retry(operation):
    for _ in range(MAX_ATTEMPTS * 5):
        try:
            return operation()
        except ServiceUnavailable:
            continue
    raise ServiceUnavailable()
