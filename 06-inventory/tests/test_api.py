import json

from tests.conftest import AUTH


def test_search_is_case_insensitive(client):
    res = client.get("/products", {"search": "widget"})
    assert res.status_code == 200
    names = [p["name"] for p in res.json()]
    assert "Widget A" in names


def test_search_partial_match(client):
    res = client.get("/products", {"search": "gadget"})
    assert res.status_code == 200
    names = [p["name"] for p in res.json()]
    assert "Gadget B" in names


def test_get_missing_product_returns_404(client):
    res = client.get("/products/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_stock_adjust_rejects_negative_qty(client):
    res = client.post(
        "/products/pr1/stock",
        data=json.dumps({"delta": -15}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400


def test_create_product_persisted(client):
    res = client.post(
        "/products",
        data=json.dumps({"name": "Cable", "qty": 3}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    product_id = res.json()["id"]
    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Cable"


def test_delete_product_with_auth(client):
    res = client.delete("/products/pr2", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/products/pr2").status_code == 404


def test_create_product_without_auth_is_401(client):
    res = client.post(
        "/products",
        data=json.dumps({"name": "Cable", "qty": 3}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_authenticated_stock_adjust(client):
    res = client.post(
        "/products/pr1/stock",
        data=json.dumps({"delta": 2}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["qty"] == 12
