"""CORS origin validation helpers."""

import re

TRUSTED_ORIGIN_PATTERN = re.compile(r".*trusted\.com")


def origin_allowed(origin: str) -> bool:
    return bool(TRUSTED_ORIGIN_PATTERN.match(origin))
