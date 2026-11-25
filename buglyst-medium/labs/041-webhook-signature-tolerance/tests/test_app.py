import json
import time

from helper import sign


def test_fresh_signature_is_accepted(client):
    body = {"event_id": "evt-fresh", "amount": 10}
    raw = json.dumps(body).encode()
    timestamp = int(time.time())
    response = client.post(
        "/webhooks",
        data=raw,
        content_type="application/json",
        headers={
            "X-Signature-Timestamp": str(timestamp),
            "X-Signature": sign(timestamp, raw),
        },
    )
    assert response.status_code == 200


def test_replay_from_hours_ago_is_rejected(client):
    body = {"event_id": "evt-replay", "amount": 20}
    raw = json.dumps(body).encode()
    timestamp = int(time.time()) - (2 * 60 * 60)
    response = client.post(
        "/webhooks",
        data=raw,
        content_type="application/json",
        headers={
            "X-Signature-Timestamp": str(timestamp),
            "X-Signature": sign(timestamp, raw),
        },
    )
    assert response.status_code == 401
    assert client.get("/_debug/processed").json()["processed"] == []
