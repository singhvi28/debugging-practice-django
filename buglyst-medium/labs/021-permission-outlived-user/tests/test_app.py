import json


def test_revoked_user_cannot_delete(client):
    headers = {"X-User-Id": "contractor-7"}
    before = client.delete("/resources/doc-42", headers=headers)
    assert before.status_code == 200

    revoke = client.post(
        "/revoke",
        data=json.dumps({"user_id": "contractor-7"}),
        content_type="application/json",
    )
    assert revoke.status_code == 200

    after = client.delete("/resources/doc-42", headers=headers)
    assert after.status_code == 403


def test_revoke_unknown_user_returns_404(client):
    res = client.post(
        "/revoke",
        data=json.dumps({"user_id": "missing"}),
        content_type="application/json",
    )
    assert res.status_code == 404
