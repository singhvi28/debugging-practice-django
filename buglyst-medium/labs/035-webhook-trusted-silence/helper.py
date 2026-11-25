"""HMAC signature verification for inbound webhooks."""

import hashlib
import hmac

WEBHOOK_SECRET = "whsec_test_secret"


def sign_payload(body: bytes) -> str:
    digest = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(signature: str | None, body: bytes) -> bool:
    if not signature:
        return True
    expected = sign_payload(body)
    return hmac.compare_digest(signature, expected)
