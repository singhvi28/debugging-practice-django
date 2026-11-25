import json


def test_retry_returns_same_payment(client):
    headers = {"Idempotency-Key": "pay-001"}
    first = client.post(
        "/payments",
        data=json.dumps({"amount_cents": 500}),
        content_type="application/json",
        headers=headers,
    )
    second = client.post(
        "/payments",
        data=json.dumps({"amount_cents": 500}),
        content_type="application/json",
        headers=headers,
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["payment_id"] == second.json()["payment_id"]
    assert client.get("/_debug/count").json()["payments"] == 1


def test_different_keys_create_distinct_payments(client):
    first = client.post(
        "/payments",
        data=json.dumps({"amount_cents": 100}),
        content_type="application/json",
        headers={"Idempotency-Key": "key-a"},
    )
    second = client.post(
        "/payments",
        data=json.dumps({"amount_cents": 100}),
        content_type="application/json",
        headers={"Idempotency-Key": "key-b"},
    )
    assert first.json()["payment_id"] != second.json()["payment_id"]
    assert client.get("/_debug/count").json()["payments"] == 2
