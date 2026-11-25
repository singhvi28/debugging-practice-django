import json

from helper import committed_value


def test_uncommitted_write_visible_inside_transaction(client):
    txn_id = "txn-1"
    client.post(f"/txn/{txn_id}/begin")
    client.post(
        f"/txn/{txn_id}/write",
        data=json.dumps({"key": "balance", "value": "100"}),
        content_type="application/json",
    )

    response = client.get(f"/txn/{txn_id}/read/balance")
    assert response.status_code == 200
    assert response.json()["value"] == "100"


def test_uncommitted_write_not_visible_outside_transaction(client):
    txn_id = "txn-2"
    client.post(f"/txn/{txn_id}/begin")
    client.post(
        f"/txn/{txn_id}/write",
        data=json.dumps({"key": "status", "value": "pending"}),
        content_type="application/json",
    )

    assert committed_value("status") is None

    client.post(f"/txn/{txn_id}/commit")
    assert committed_value("status") == "pending"


def test_rollback_discards_buffered_write(client):
    txn_id = "txn-3"
    client.post(f"/txn/{txn_id}/begin")
    client.post(
        f"/txn/{txn_id}/write",
        data=json.dumps({"key": "flag", "value": "on"}),
        content_type="application/json",
    )
    client.post(f"/txn/{txn_id}/rollback")

    response = client.get(f"/txn/{txn_id}/read/flag")
    assert response.json()["value"] is None
    assert committed_value("flag") is None
