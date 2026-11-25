import json

SECRET = "sk_live_super_secret_key"


def test_invalid_amount_does_not_leak_authorization(client):
    response = client.post(
        "/charge",
        data=json.dumps({"amount_cents": 0}),
        content_type="application/json",
        headers={"Authorization": SECRET},
    )
    assert response.status_code == 402
    detail = response.json()["detail"]
    assert SECRET not in detail
    assert "authorization" not in detail.lower()


def test_bad_prefix_does_not_leak_authorization(client):
    response = client.post(
        "/charge",
        data=json.dumps({"amount_cents": 100}),
        content_type="application/json",
        headers={"Authorization": "pk_test_public_only"},
    )
    assert response.status_code == 402
    assert "pk_test_public_only" not in response.json()["detail"]
