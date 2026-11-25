def test_reordered_json_body_hits_same_operation(client):
    first = client.post(
        "/operations",
        data={"account": "acct-1", "amount": 25.0, "currency": "USD"},
        content_type="application/json",
    )
    second = client.post(
        "/operations",
        data={"amount": 25.0, "currency": "USD", "account": "acct-1"},
        content_type="application/json",
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["operation_id"] == second.json()["operation_id"]


def test_different_amounts_create_distinct_operations(client):
    first = client.post("/operations", data={"account": "acct-2", "amount": 10.0}, content_type="application/json")
    second = client.post("/operations", data={"account": "acct-2", "amount": 11.0}, content_type="application/json")
    assert first.json()["operation_id"] != second.json()["operation_id"]
