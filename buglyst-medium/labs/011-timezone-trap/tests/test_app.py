def test_late_utc_evening_stays_on_same_utc_day(client):
    response = client.get("/report", {"at": "2024-06-15T23:30:00Z"})
    assert response.status_code == 200
    assert response.json()["day"] == "2024-06-15"


def test_utc_midnight_starts_new_day(client):
    response = client.get("/report", {"at": "2024-06-16T00:15:00Z"})
    assert response.json()["day"] == "2024-06-16"


def test_offset_timestamp_uses_utc_bucket(client):
    response = client.get("/report", {"at": "2024-01-01T00:30:00+00:00"})
    assert response.json()["day"] == "2024-01-01"
