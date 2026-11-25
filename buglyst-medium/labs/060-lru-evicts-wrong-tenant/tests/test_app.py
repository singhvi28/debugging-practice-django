def test_lru_evicts_least_recently_used(client):
    tenant = "acme"
    client.put(f"/cache/{tenant}/a", data={"value": "1"}, content_type="application/json")
    client.put(f"/cache/{tenant}/b", data={"value": "2"}, content_type="application/json")
    client.put(f"/cache/{tenant}/c", data={"value": "3"}, content_type="application/json")
    client.get(f"/cache/{tenant}/a")
    client.put(f"/cache/{tenant}/d", data={"value": "4"}, content_type="application/json")
    keys = client.get(f"/cache/{tenant}/_keys").json()["keys"]
    assert "a" in keys
    assert "b" not in keys


def test_mru_entry_survives_capacity_pressure(client):
    tenant = "beta"
    client.put(f"/cache/{tenant}/x", data={"value": "x"}, content_type="application/json")
    client.put(f"/cache/{tenant}/y", data={"value": "y"}, content_type="application/json")
    client.put(f"/cache/{tenant}/z", data={"value": "z"}, content_type="application/json")
    client.get(f"/cache/{tenant}/z")
    client.put(f"/cache/{tenant}/w", data={"value": "w"}, content_type="application/json")
    res = client.get(f"/cache/{tenant}/z")
    assert res.status_code == 200


def test_capacity_limits_entries(client):
    tenant = "gamma"
    for name in ["one", "two", "three", "four"]:
        client.put(f"/cache/{tenant}/{name}", data={"value": name}, content_type="application/json")
    keys = client.get(f"/cache/{tenant}/_keys").json()["keys"]
    assert len(keys) == 3
