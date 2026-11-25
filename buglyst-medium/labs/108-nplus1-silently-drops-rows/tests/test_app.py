def test_every_order_is_enriched_with_user_details(client):
    response = client.get("/orders/enriched")
    payload = response.json()

    assert response.status_code == 200
    assert payload["count"] == 2
    assert {order["order_id"] for order in payload["orders"]} == {101, 102}
    assert {order["user_name"] for order in payload["orders"]} == {"Ada", "Lin"}


def test_enriched_payload_keeps_user_ids(client):
    response = client.get("/orders/enriched")
    orders = response.json()["orders"]

    assert sorted(order["user_id"] for order in orders) == [1, 2]
