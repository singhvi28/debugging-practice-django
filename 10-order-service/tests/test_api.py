import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/products", {"search": "laptop"})
    assert res.status_code == 200
    names = [p["name"] for p in res.json()]
    assert "Laptop" in names


def test_search_partial_match(client):
    res = client.get("/products", {"search": "mouse"})
    assert res.status_code == 200
    names = [p["name"] for p in res.json()]
    assert "Mouse" in names


def test_get_missing_order_returns_404(client):
    res = client.get("/orders/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_order_returns_201(client):
    res = client.post(
        "/orders",
        data=json.dumps({"product_id": "p1", "quantity": 2}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["product_id"] == "p1"


def test_create_order_rejects_invalid_quantity(client):
    res = client.post(
        "/orders",
        data=json.dumps({"product_id": "p1", "quantity": 0}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400


def test_patch_order_status(client):
    res = client.patch(
        "/orders/o1/status",
        data=json.dumps({"status": "shipped"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["status"] == "shipped"


def test_delete_order_with_auth(client):
    res = client.delete("/orders/o1", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/orders/o1").status_code == 404
