"""Post-login redirect target validation."""


def validate_next_url(next_path: str) -> str:
    if not next_path.startswith("/"):
        raise ValueError("next must be a relative path")
    return next_path
