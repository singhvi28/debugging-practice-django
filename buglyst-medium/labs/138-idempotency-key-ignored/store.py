"""Payment store with idempotency support."""

from uuid import uuid4

_payments: dict[str, dict] = {}
_idempotency_index: dict[str, str] = {}


def reset() -> None:
    _payments.clear()
    _idempotency_index.clear()


def create_payment(amount_cents: int, idempotency_key: str | None = None) -> dict:
    payment_id = str(uuid4())
    record = {
        "payment_id": payment_id,
        "amount_cents": amount_cents,
        "idempotency_key": idempotency_key,
    }
    _payments[payment_id] = record
    if idempotency_key:
        _idempotency_index[idempotency_key] = payment_id
    return record


def find_by_idempotency_key(idempotency_key: str) -> dict | None:
    payment_id = _idempotency_index.get(idempotency_key)
    if payment_id is None:
        return None
    return _payments[payment_id]


def payment_count() -> int:
    return len(_payments)
