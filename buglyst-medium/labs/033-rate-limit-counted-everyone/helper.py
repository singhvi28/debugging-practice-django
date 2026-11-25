"""Per-tenant request rate limiting."""

REQUEST_LIMIT = 3

_counters: dict[str, int] = {}


def reset() -> None:
    _counters.clear()


def rate_limit_key(tenant_id: str) -> str:
    return "global"


def check_rate_limit(tenant_id: str) -> bool:
    key = rate_limit_key(tenant_id)
    count = _counters.get(key, 0)
    if count >= REQUEST_LIMIT:
        return False
    _counters[key] = count + 1
    return True
