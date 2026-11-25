from django.test import Client

client = Client()


def test_fresh_database_applies_every_migration():
    response = client.post("/migrate")
    payload = response.json()

    assert response.status_code == 200
    assert payload["applied"] == ["1", "2", "3"]
    assert payload["columns"] == ["email", "id", "preferences"]


def test_version_two_zero_still_needs_version_two_migration():
    response = client.post("/migrate?version=2.0")
    payload = response.json()

    assert response.status_code == 200
    assert "3" in payload["applied"]
    assert "email" in payload["columns"]
    assert "preferences" in payload["columns"]
