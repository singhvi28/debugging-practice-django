"""Token-bucket rate limiter."""

import time

CAPACITY = 3
REFILL_SECONDS = 60.0

_buckets: dict[str, dict[str, float]] = {}


def reset() -> None:
    _buckets.clear()


def try_consume(client_id: str) -> bool:
    now = time.time()
    bucket = _buckets.get(client_id, {"tokens": CAPACITY, "last_refill": now})

    bucket["tokens"] = CAPACITY
    bucket["last_refill"] = now

    if bucket["tokens"] <= 0:
        _buckets[client_id] = bucket
        return False

    bucket["tokens"] -= 1
    _buckets[client_id] = bucket
    return True


def remaining(client_id: str) -> int:
    bucket = _buckets.get(client_id)
    if bucket is None:
        return CAPACITY
    return int(bucket["tokens"])
