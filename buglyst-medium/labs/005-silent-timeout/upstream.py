"""Simulated slow upstream dependency."""

import time

SLOW_DELAY_SECONDS = 0.5


def reset() -> None:
    pass


def fetch_upstream() -> dict:
    time.sleep(SLOW_DELAY_SECONDS)
    return {"payload": "ok"}
