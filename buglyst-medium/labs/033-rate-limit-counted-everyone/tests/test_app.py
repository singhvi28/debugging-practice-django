def test_tenant_hits_own_limit(client):
    for _ in range(3):
        assert client.get("/api/data", HTTP_X_TENANT_ID="acme").status_code == 200
    assert client.get("/api/data", HTTP_X_TENANT_ID="acme").status_code == 429


def test_other_tenants_are_not_blocked(client):
    for _ in range(3):
        assert client.get("/api/data", HTTP_X_TENANT_ID="east").status_code == 200
    assert client.get("/api/data", HTTP_X_TENANT_ID="east").status_code == 429
    assert client.get("/api/data", HTTP_X_TENANT_ID="west").status_code == 200
