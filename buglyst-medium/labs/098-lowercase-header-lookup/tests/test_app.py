def test_lowercase_authorization_header_is_accepted(client):
    response = client.get(
        "/protected",
        headers={"authorization": "Bearer service-token"},
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["authorized"] is True
    assert payload["subject"] == "api-client"


def test_missing_header_stays_unauthorized(client):
    response = client.get("/protected")
    payload = response.json()

    assert response.status_code == 200
    assert payload["authorized"] is False
