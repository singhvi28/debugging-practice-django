import json

from helper import sign_payload


def test_signed_webhook_is_accepted(client):
    body = {"event_id": "evt-1", "amount": 10}
    raw = json.dumps(body).encode()
    response = client.post(
        "/webhooks",
        data=raw,
        content_type="application/json",
        HTTP_X_SIGNATURE=sign_payload(raw),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "processed"


def test_missing_signature_is_rejected(client):
    body = {"event_id": "evt-2", "amount": 20}
    response = client.post(
        "/webhooks",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 401
    assert client.get("/_debug/processed").json()["processed"] == []
