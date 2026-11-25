import json

from tests.conftest import AUTH


def test_authenticated_create_persists(client):
    res = client.post(
        "/appointments",
        data=json.dumps({
            "provider_id": "prov_1",
            "patient_name": "Alice",
            "start_at": "2026-03-15T10:00:00+00:00",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    appt_id = res.json()["id"]
    assert appt_id != "pending"
    fetched = client.get(f"/appointments/{appt_id}")
    assert fetched.status_code == 200
    assert fetched.json()["patient_name"] == "Alice"


def test_patch_appointment_notes(client):
    created = client.post(
        "/appointments",
        data=json.dumps({
            "provider_id": "prov_1",
            "patient_name": "Bob",
            "start_at": "2026-03-16T11:00:00+00:00",
        }),
        content_type="application/json",
        headers=AUTH,
    ).json()
    res = client.patch(
        f"/appointments/{created['id']}",
        data=json.dumps({"notes": "Follow-up"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["notes"] == "Follow-up"


def test_double_book_same_slot_returns_409(client):
    payload = {
        "provider_id": "prov_1",
        "patient_name": "First",
        "start_at": "2026-03-17T09:00:00+00:00",
    }
    first = client.post(
        "/appointments",
        data=json.dumps(payload),
        content_type="application/json",
        headers=AUTH,
    )
    assert first.status_code == 201
    second = client.post(
        "/appointments",
        data=json.dumps({**payload, "patient_name": "Second"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert second.status_code == 409


def test_list_appointments_by_utc_date(client):
    client.post(
        "/appointments",
        data=json.dumps({
            "provider_id": "prov_2",
            "patient_name": "UTC Edge",
            "start_at": "2026-04-01T00:30:00+00:00",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    res = client.get("/appointments", {"date": "2026-04-01"})
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["patient_name"] == "UTC Edge"


def test_cancel_frees_provider_slot(client):
    created = client.post(
        "/appointments",
        data=json.dumps({
            "provider_id": "prov_1",
            "patient_name": "Cancel Me",
            "start_at": "2026-03-18T14:00:00+00:00",
        }),
        content_type="application/json",
        headers=AUTH,
    ).json()
    cancel = client.post(f"/appointments/{created['id']}/cancel", headers=AUTH)
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "canceled"
    assert cancel.json()["slot_booked"] is False
    rebook = client.post(
        "/appointments",
        data=json.dumps({
            "provider_id": "prov_1",
            "patient_name": "Rebook",
            "start_at": "2026-03-18T14:00:00+00:00",
        }),
        content_type="application/json",
        headers=AUTH,
    )
    assert rebook.status_code == 201
