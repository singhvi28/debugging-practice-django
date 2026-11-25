"""Request-body fingerprinting for idempotent operations."""

import json

_cache: dict[str, dict] = {}
_next_op_id = 1


def reset() -> None:
    global _next_op_id
    _cache.clear()
    _next_op_id = 1


def fingerprint(body: dict) -> str:
    return json.dumps(body)


def lookup(fingerprint_key: str) -> dict | None:
    return _cache.get(fingerprint_key)


def save(fingerprint_key: str, record: dict) -> None:
    _cache[fingerprint_key] = record


def next_operation_id() -> int:
    global _next_op_id
    op_id = _next_op_id
    _next_op_id += 1
    return op_id
