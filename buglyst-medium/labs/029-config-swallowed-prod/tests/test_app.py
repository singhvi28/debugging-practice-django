def test_prod_uses_prod_database_url(client):
    res = client.get("/config")
    assert res.status_code == 200
    body = res.json()
    assert body["ENVIRONMENT"] == "prod"
    assert "app_prod" in body["DATABASE_URL"]
    assert body["DEBUG"] == "false"


def test_prod_does_not_use_dev_database(client):
    res = client.get("/config")
    assert "app_dev" not in res.json()["DATABASE_URL"]
