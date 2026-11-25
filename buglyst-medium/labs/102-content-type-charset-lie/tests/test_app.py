import json


def test_latin1_payload_decodes_using_declared_charset(client):
    raw = "café".encode("latin-1")
    response = client.post(
        "/decode",
        data=json.dumps(
            {
                "content": raw.hex(),
                "content_type": "text/plain; charset=latin-1",
            }
        ),
        content_type="application/json",
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["text"] == "café"


def test_utf8_payload_still_decodes(client):
    raw = "café".encode("utf-8")
    response = client.post(
        "/decode",
        data=json.dumps(
            {
                "content": raw.hex(),
                "content_type": "text/plain; charset=utf-8",
            }
        ),
        content_type="application/json",
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["text"] == "café"
