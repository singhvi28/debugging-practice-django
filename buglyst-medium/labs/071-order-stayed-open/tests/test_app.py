import json


def test_successful_order_deducts_inventory(client):
    response = client.post(
        "/orders",
        data=json.dumps({"items": [{"sku": "widget", "quantity": 2}]}),
        content_type="application/json",
    )
    assert response.status_code == 200

    inventory = client.get("/inventory").json()
    assert inventory["widget"] == 3

    orders = client.get("/orders").json()["orders"]
    assert len(orders) == 1


def test_failed_deduction_does_not_leave_an_order(client):
    response = client.post(
        "/orders",
        data=json.dumps({"items": [{"sku": "widget", "quantity": 99}]}),
        content_type="application/json",
    )
    assert response.status_code == 400

    orders = client.get("/orders").json()["orders"]
    assert orders == []

    inventory = client.get("/inventory").json()
    assert inventory["widget"] == 5


def test_partial_failure_rolls_back_entire_order(client):
    response = client.post(
        "/orders",
        data=json.dumps(
            {
                "items": [
                    {"sku": "widget", "quantity": 1},
                    {"sku": "gadget", "quantity": 99},
                ]
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert client.get("/orders").json()["orders"] == []
    assert client.get("/inventory").json() == {"widget": 5, "gadget": 3}
