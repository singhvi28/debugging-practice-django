"""CORS header helpers."""

ALLOWED_ORIGIN = "https://app.example.com"
ALLOWED_METHODS = "GET,OPTIONS"
EXPOSE_HEADERS = "X-Request-Id, X-RateLimit-Remaining"


def apply_cors_headers(headers: dict[str, str], origin: str, *, is_preflight: bool) -> dict[str, str]:
    updated = dict(headers)
    if origin != ALLOWED_ORIGIN:
        return updated

    updated["Access-Control-Allow-Origin"] = origin
    updated["Access-Control-Allow-Methods"] = ALLOWED_METHODS
    updated["Vary"] = "Origin"

    if not is_preflight:
        updated["Access-Control-Expose-Headers"] = EXPOSE_HEADERS

    return updated
