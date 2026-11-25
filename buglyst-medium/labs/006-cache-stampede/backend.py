"""Simulated expensive backend."""

import time

_fetch_count = 0
FETCH_DELAY_SECONDS = 0.02


def reset() -> None:
    global _fetch_count
    _fetch_count = 0


def fetch_value() -> str:
    global _fetch_count
    _fetch_count += 1
    time.sleep(FETCH_DELAY_SECONDS)
    return "daily-report"


def get_fetch_count() -> int:
    return _fetch_count
