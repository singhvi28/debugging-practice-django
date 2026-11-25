"""Idempotent payment record storage."""

_records: dict[str, dict] = {}
_next_charge_id = 1


class AmountMismatchError(Exception):
    """Raised when an idempotency key is reused with a different amount."""


def reset() -> None:
    global _next_charge_id
    _records.clear()
    _next_charge_id = 1


def lookup(key: str, amount: float) -> dict | None:
    record = _records.get(key)
    if record is None:
        return None
    return record


def save(key: str, record: dict) -> None:
    _records[key] = record


def next_charge_id() -> int:
    global _next_charge_id
    charge_id = _next_charge_id
    _next_charge_id += 1
    return charge_id
