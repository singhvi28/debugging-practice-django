"""Case-sensitive header lookup used by auth middleware."""


def get_header(headers: dict[str, str], name: str) -> str | None:
    return headers.get(name)
