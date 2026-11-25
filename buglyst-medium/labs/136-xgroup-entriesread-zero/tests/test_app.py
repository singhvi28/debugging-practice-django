import json


def test_entriesread_zero_is_emitted_for_create(client):
    response = client.post(
        "/xgroup/args",
        data=json.dumps(
            {
                "command": "CREATE",
                "stream": "events",
                "group": "workers",
                "stream_id": "0",
                "entries_read": 0,
            }
        ),
        content_type="application/json",
    )
    assert response.json()["tokens"] == [
        "XGROUP",
        "CREATE",
        "events",
        "workers",
        "0",
        "ENTRIESREAD",
        "0",
    ]


def test_entriesread_zero_is_emitted_for_setid(client):
    response = client.post(
        "/xgroup/args",
        data=json.dumps(
            {
                "command": "SETID",
                "stream": "events",
                "group": "workers",
                "stream_id": "0-0",
                "entries_read": 0,
            }
        ),
        content_type="application/json",
    )
    tokens = response.json()["tokens"]
    assert tokens[-2:] == ["ENTRIESREAD", "0"]
