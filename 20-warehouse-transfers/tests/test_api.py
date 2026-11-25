import json

from tests.conftest import AUTH


def test_create_transfer_with_auth(client):
    res = client.post(
        "/transfers",
        data=json.dumps({
            "sku": "SKU-100",
            "quantity": 10,
            "from_location_id": "wh_east",
            "to_location_id": "wh_west",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    transfer_id = res.json()["id"]
    fetched = client.get(f"/transfers/{transfer_id}")
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "completed"


def test_transfer_updates_destination_stock(client):
    client.post(
        "/transfers",
        data=json.dumps({
            "sku": "SKU-200",
            "quantity": 4,
            "from_location_id": "wh_east",
            "to_location_id": "wh_west",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    res = client.get("/locations/wh_west/stock/SKU-200")
    assert res.status_code == 200
    assert res.json()["quantity"] == 4


def test_insufficient_stock_returns_409_without_dest_change(client):
    before = client.get("/locations/wh_west/stock/SKU-100").json()["quantity"]
    res = client.post(
        "/transfers",
        data=json.dumps({
            "sku": "SKU-100",
            "quantity": 999,
            "from_location_id": "wh_east",
            "to_location_id": "wh_west",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409
    after = client.get("/locations/wh_west/stock/SKU-100").json()["quantity"]
    assert after == before


def test_get_stock_missing_location_returns_404(client):
    res = client.get("/locations/missing/stock")
    assert res.status_code == 404


def test_transfer_persists_record(client):
    res = client.post(
        "/transfers",
        data=json.dumps({
            "sku": "SKU-100",
            "quantity": 3,
            "from_location_id": "wh_east",
            "to_location_id": "wh_west",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["status"] == "completed"
    transfer_id = res.json()["id"]
    assert client.get(f"/transfers/{transfer_id}").status_code == 200
