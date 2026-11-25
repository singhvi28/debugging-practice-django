def test_orchestrator_region_overrides_baked_in_default(client):
    response = client.post("/deploy/region?region=eu-west-1")
    payload = response.json()

    assert response.status_code == 200
    assert payload["region"] == "eu-west-1"
    assert payload["source"] == "orchestrator"


def test_default_region_when_orchestrator_omits_value(client):
    response = client.post("/deploy/region")
    payload = response.json()

    assert response.status_code == 200
    assert payload["region"] == "us-east-1"
    assert payload["source"] == "default"
