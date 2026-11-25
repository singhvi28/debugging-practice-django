def test_miss_then_create_then_get_returns_record(client):
    miss = client.get("/records/user-42")
    assert miss.status_code == 404
    create = client.post("/records/user-42", data={"value": "alice"}, content_type="application/json")
    assert create.status_code == 200
    get = client.get("/records/user-42")
    assert get.status_code == 200
    assert get.json()["value"] == "alice"


def test_create_then_get_without_prior_miss(client):
    client.post("/records/item-7", data={"value": "widget"}, content_type="application/json")
    res = client.get("/records/item-7")
    assert res.status_code == 200
    assert res.json()["value"] == "widget"


def test_second_get_after_create_still_finds_record(client):
    client.get("/records/ghost")
    client.post("/records/ghost", data={"value": "visible"}, content_type="application/json")
    first = client.get("/records/ghost")
    second = client.get("/records/ghost")
    assert first.status_code == 200
    assert second.status_code == 200
