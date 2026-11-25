import json


def test_single_webhook_processed_once(client):
    body = {"event_id": "evt-1", "payload": {"ok": True}}
    response = client.post(
        "/webhooks",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200
    processed = client.get("/_debug/processed").json()["processed"]
    assert processed.count("evt-1") == 1


def test_later_webhooks_are_not_multiplied_by_prior_registrations(client):
    for event_id in ("evt-a", "evt-b", "evt-c"):
        client.post(
            "/webhooks",
            data=json.dumps({"event_id": event_id, "payload": {}}),
            content_type="application/json",
        )

    processed = client.get("/_debug/processed").json()["processed"]
    assert processed.count("evt-a") == 1
    assert processed.count("evt-b") == 1
    assert processed.count("evt-c") == 1
