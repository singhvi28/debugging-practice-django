def test_include_deleted_false_excludes_soft_deleted(client):
    res = client.get("/items", {"includeDeleted": "false"})
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) == 2
    assert all(not item["deleted"] for item in items)
    assert {item["id"] for item in items} == {"item-1", "item-3"}


def test_include_deleted_true_returns_all(client):
    res = client.get("/items", {"includeDeleted": "true"})
    assert res.status_code == 200
    assert len(res.json()["items"]) == 3


def test_omitted_param_excludes_soft_deleted(client):
    res = client.get("/items")
    assert res.status_code == 200
    assert all(not item["deleted"] for item in res.json()["items"])
