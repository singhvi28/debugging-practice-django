import json


def test_write_then_read_same_tenant(client):
    client.put(
        "/kv/acme/config",
        data=json.dumps({"value": "prod"}),
        content_type="application/json",
    )
    res = client.get("/kv/acme/config")
    assert res.status_code == 200
    assert res.json()["value"] == "prod"


def test_tenants_with_same_key_are_isolated(client):
    client.put(
        "/kv/acme/theme",
        data=json.dumps({"value": "blue"}),
        content_type="application/json",
    )
    client.put(
        "/kv/beta/theme",
        data=json.dumps({"value": "red"}),
        content_type="application/json",
    )
    acme = client.get("/kv/acme/theme")
    beta = client.get("/kv/beta/theme")
    assert acme.json()["value"] == "blue"
    assert beta.json()["value"] == "red"


def test_different_keys_same_tenant(client):
    client.put(
        "/kv/gamma/a",
        data=json.dumps({"value": "first"}),
        content_type="application/json",
    )
    client.put(
        "/kv/gamma/b",
        data=json.dumps({"value": "second"}),
        content_type="application/json",
    )
    assert client.get("/kv/gamma/a").json()["value"] == "first"
    assert client.get("/kv/gamma/b").json()["value"] == "second"
