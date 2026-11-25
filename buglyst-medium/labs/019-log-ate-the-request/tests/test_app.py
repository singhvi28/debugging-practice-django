import json

SENSITIVE_PAYLOAD = {
    "name": "Quarterly report",
    "ssn": "123-45-6789",
    "card": "4111-1111-1111-1111",
}


def test_upload_succeeds(client):
    response = client.post(
        "/upload",
        data=json.dumps(SENSITIVE_PAYLOAD),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["received"] is True


def test_logs_do_not_contain_ssn(client, capture_upload_logs):
    client.post(
        "/upload",
        data=json.dumps(SENSITIVE_PAYLOAD),
        content_type="application/json",
    )
    messages = " ".join(record.getMessage() for record in capture_upload_logs)
    assert "123-45-6789" not in messages


def test_logs_do_not_contain_card_number(client, capture_upload_logs):
    client.post(
        "/upload",
        data=json.dumps(SENSITIVE_PAYLOAD),
        content_type="application/json",
    )
    messages = " ".join(record.getMessage() for record in capture_upload_logs)
    assert "4111-1111-1111-1111" not in messages
