def test_orders_scoped_to_tenant(client):
    res = client.get("/orders", HTTP_X_TENANT_ID="tenant-a")
    assert res.status_code == 200
    body = res.json()
    assert body["tenant_id"] == "tenant-a"
    assert len(body["orders"]) == 2
    assert all(order["tenant_id"] == "tenant-a" for order in body["orders"])


def test_other_tenant_sees_only_its_orders(client):
    res = client.get("/orders", HTTP_X_TENANT_ID="tenant-c")
    assert res.status_code == 200
    body = res.json()
    assert len(body["orders"]) == 1
    assert body["orders"][0]["id"] == "o-5"
