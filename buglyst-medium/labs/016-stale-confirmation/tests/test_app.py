import json


def test_put_returns_updated_value(client):
    client.get("/items/widget")
    response = client.put(
        "/items/widget",
        data=json.dumps({"value": "v2"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["value"] == "v2"


def test_get_reflects_update_after_put(client):
    client.get("/items/widget")
    client.put(
        "/items/widget",
        data=json.dumps({"value": "v3"}),
        content_type="application/json",
    )
    response = client.get("/items/widget")
    assert response.json()["value"] == "v3"


def test_confirmation_matches_persisted_state(client):
    client.get("/items/widget")
    client.put(
        "/items/widget",
        data=json.dumps({"value": "v4"}),
        content_type="application/json",
    )
    response = client.get("/items/widget")
    assert response.json()["value"] == "v4"
