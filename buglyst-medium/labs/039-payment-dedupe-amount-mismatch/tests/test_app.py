KEY = "pay-7a3b-9c2d"


def test_retry_with_same_key_and_amount_returns_same_record(client):
    headers = {"Idempotency-Key": KEY}
    body = {"amount": 42.0, "currency": "USD"}
    first = client.post("/payments", data=body, content_type="application/json", headers=headers)
    second = client.post("/payments", data=body, content_type="application/json", headers=headers)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["charge_id"] == second.json()["charge_id"]


def test_same_key_with_different_amount_returns_conflict(client):
    headers = {"Idempotency-Key": KEY}
    first = client.post("/payments", data={"amount": 42.0}, content_type="application/json", headers=headers)
    second = client.post("/payments", data={"amount": 99.0}, content_type="application/json", headers=headers)
    assert first.status_code == 200
    assert second.status_code == 409
