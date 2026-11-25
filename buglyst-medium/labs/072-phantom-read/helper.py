"""Simulated transaction buffer over an in-memory key-value store."""

_store: dict[str, str] = {}
_pending: dict[str, dict[str, str]] = {}


def reset() -> None:
    _store.clear()
    _pending.clear()


def begin(txn_id: str) -> None:
    _pending[txn_id] = {}


def write(txn_id: str, key: str, value: str) -> None:
    if txn_id not in _pending:
        raise KeyError(f"unknown transaction: {txn_id}")
    _pending[txn_id][key] = value


def read(txn_id: str, key: str) -> str | None:
    return _store.get(key)


def commit(txn_id: str) -> None:
    buffer = _pending.pop(txn_id, {})
    _store.update(buffer)


def rollback(txn_id: str) -> None:
    _pending.pop(txn_id, None)


def committed_value(key: str) -> str | None:
    return _store.get(key)
