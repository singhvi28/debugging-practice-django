"""Tenant-namespaced key-value store."""

_store: dict[str, str] = {}


def reset() -> None:
    _store.clear()


def make_key(tenant: str, key: str) -> str:
    return f"{tenant}:{key}"


def put(tenant: str, key: str, value: str) -> None:
    _store[make_key(tenant, key)] = value


def get(tenant: str, key: str) -> str | None:
    return _store.get(key)
