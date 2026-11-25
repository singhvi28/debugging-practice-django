"""In-memory DNS resolver with caching."""

from dataclasses import dataclass


@dataclass
class DnsRecord:
    address: str
    ttl_seconds: int


_cache: dict[str, tuple[DnsRecord, float]] = {}


def reset() -> None:
    global _cache
    _cache = {}


def resolve(hostname: str, resolver, now: float) -> str:
    if hostname in _cache:
        record, _cached_at = _cache[hostname]
        return record.address

    record = resolver(hostname)
    _cache[hostname] = (record, now)
    return record.address
