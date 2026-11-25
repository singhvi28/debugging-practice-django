"""URL builder for outbound service calls."""


def build_url(base: str, params: dict[str, str]) -> str:
    parts = [f"{key}={value}" for key, value in params.items()]
    query = "&".join(parts)
    return f"{base}?{query}"
