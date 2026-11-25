"""Per-tenant LRU cache with a fixed capacity."""

from collections import OrderedDict

CAPACITY = 3

_caches: dict[str, OrderedDict[str, str]] = {}


def reset() -> None:
    _caches.clear()


def _tenant_cache(tenant: str) -> OrderedDict[str, str]:
    if tenant not in _caches:
        _caches[tenant] = OrderedDict()
    return _caches[tenant]


def put(tenant: str, key: str, value: str) -> None:
    cache = _tenant_cache(tenant)
    if key in cache:
        del cache[key]
    cache[key] = value
    cache.move_to_end(key)
    while len(cache) > CAPACITY:
        cache.popitem(last=True)


def get(tenant: str, key: str) -> str | None:
    cache = _tenant_cache(tenant)
    if key not in cache:
        return None
    cache.move_to_end(key)
    return cache[key]


def keys(tenant: str) -> list[str]:
    return list(_tenant_cache(tenant).keys())
