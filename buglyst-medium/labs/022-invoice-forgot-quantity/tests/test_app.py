import json


def test_invoice_total_multiplies_price_by_quantity(client):
    payload = {
        "customer_id": "cust-1",
        "lines": [
            {"sku": "widget", "price": 10.0, "qty": 3},
            {"sku": "gizmo", "price": 5.5, "qty": 2},
        ],
    }
    res = client.post(
        "/invoice",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["total"] == 41.0


def test_single_quantity_line(client):
    payload = {
        "customer_id": "cust-2",
        "lines": [{"sku": "bolt", "price": 2.25, "qty": 1}],
    }
    res = client.post(
        "/invoice",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["total"] == 2.25
