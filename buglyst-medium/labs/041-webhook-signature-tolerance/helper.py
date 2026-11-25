"""Signed webhook verification with timestamp tolerance."""

import hashlib
import hmac
import time

WEBHOOK_SECRET = "whsec_tolerance_test"

TOLERANCE_MINUTES = 5
TOLERANCE_SECONDS = TOLERANCE_MINUTES * 24 * 60 * 60


def sign(timestamp: int, body: bytes) -> str:
    message = f"{timestamp}.".encode() + body
    digest = hmac.new(WEBHOOK_SECRET.encode(), message, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify(timestamp: int, signature: str, body: bytes) -> bool:
    now = int(time.time())
    if abs(now - timestamp) > TOLERANCE_SECONDS:
        return False
    expected = sign(timestamp, body)
    return hmac.compare_digest(signature, expected)
