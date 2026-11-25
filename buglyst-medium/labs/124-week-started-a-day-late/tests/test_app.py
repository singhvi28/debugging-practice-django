import json


def test_monday_stays_in_its_iso_week(client):
    response = client.post(
        "/events/bucket",
        data=json.dumps({"event_date": "2025-01-06"}),
        content_type="application/json",
    )
    assert response.json()["week_start"] == "2025-01-06"


def test_sunday_belongs_to_previous_iso_week(client):
    response = client.post(
        "/events/bucket",
        data=json.dumps({"event_date": "2025-01-05"}),
        content_type="application/json",
    )
    assert response.json()["week_start"] == "2024-12-30"
