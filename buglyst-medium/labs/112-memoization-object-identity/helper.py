"""Memoized catalog search queries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchQuery:
    term: str
    category: str


_cache: dict[int, list[str]] = {}
_call_count = 0


def reset() -> None:
    global _cache, _call_count
    _cache = {}
    _call_count = 0


def search_catalog(query: SearchQuery) -> dict:
    global _call_count

    cache_key = id(query)
    if cache_key in _cache:
        return {"results": _cache[cache_key], "cache_hit": True, "calls": _call_count}

    _call_count += 1
    results = [f"{query.category}:{query.term}"]
    _cache[cache_key] = results
    return {"results": results, "cache_hit": False, "calls": _call_count}
