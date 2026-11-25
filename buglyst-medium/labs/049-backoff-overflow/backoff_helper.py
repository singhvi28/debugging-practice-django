"""Exponential backoff delay calculator."""

BASE_MS = 100.0
MAX_DELAY_MS = 30000.0


def compute_delay_ms(attempt: int) -> float:
    """Return the backoff delay in milliseconds for a given attempt number."""
    return BASE_MS * (2.0 ** attempt)
