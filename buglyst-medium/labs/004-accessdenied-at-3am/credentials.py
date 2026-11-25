"""Credential loader with in-memory secret rotation."""

_current_secret = "secret-v1"
_cached_secret: str | None = None


def reset() -> None:
    global _current_secret, _cached_secret
    _current_secret = "secret-v1"
    _cached_secret = None


def get_secret() -> str:
    global _cached_secret
    if _cached_secret is None:
        _cached_secret = _current_secret
    return _cached_secret


def rotate_secret(new_secret: str) -> None:
    global _current_secret
    _current_secret = new_secret
