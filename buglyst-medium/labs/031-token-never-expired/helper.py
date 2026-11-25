"""Session token storage and validation."""

import secrets
import time

_sessions: dict[str, dict] = {}


def reset() -> None:
    _sessions.clear()


def create_session(subject: str, ttl_seconds: int) -> str:
    token = secrets.token_urlsafe(16)
    expires_at = int(time.time()) + ttl_seconds
    _sessions[token] = {
        "subject": subject,
        "expiresAt": expires_at,
        "active": True,
    }
    return token


def validate_session(token: str) -> dict | None:
    session = _sessions.get(token)
    if session is None or not session.get("active"):
        return None
    return session
