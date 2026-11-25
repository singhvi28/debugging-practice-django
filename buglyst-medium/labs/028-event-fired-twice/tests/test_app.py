import json


def test_single_delivery_without_reconnect(client):
    res = client.post(
        "/event",
        data=json.dumps({"type": "order.created", "id": "evt-1"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    deliveries = client.get("/webhooks").json()["deliveries"]
    assert len(deliveries) == 1
    assert deliveries[0]["id"] == "evt-1"


def test_reconnect_does_not_duplicate_delivery(client):
    client.post("/reconnect")
    client.post(
        "/event",
        data=json.dumps({"type": "order.created", "id": "evt-2"}),
        content_type="application/json",
    )
    deliveries = client.get("/webhooks").json()["deliveries"]
    assert len(deliveries) == 1
    assert deliveries[0]["id"] == "evt-2"
