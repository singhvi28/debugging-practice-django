import time

from helper import PROVIDER_RETRY_WINDOW_SEC


def test_burst_then_retry_deduplicates_first_event(client):
    for event_id in ("evt-a", "evt-b", "evt-c"):
        response = client.post("/webhooks", data={"event_id": event_id, "payload": {"n": 1}}, content_type="application/json")
        assert response.json()["status"] == "processed"

    time.sleep(PROVIDER_RETRY_WINDOW_SEC / 2)

    retry = client.post("/webhooks", data={"event_id": "evt-a", "payload": {"n": 1}}, content_type="application/json")
    assert retry.json()["status"] == "duplicate"
    processed = client.get("/_debug/processed").json()["processed"]
    assert processed.count("evt-a") == 1
