import json


def test_skipped_job_does_not_drop_following_job(client):
    body = {
        "jobs": [
            {"id": "skip-me", "skip": True},
            {"id": "run-me", "skip": False},
        ]
    }
    response = client.post(
        "/jobs/run",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["completed"] == ["run-me"]


def test_multiple_skips_still_process_later_jobs(client):
    body = {
        "jobs": [
            {"id": "a", "skip": True},
            {"id": "b", "skip": False},
            {"id": "c", "skip": True},
            {"id": "d", "skip": False},
        ]
    }
    response = client.post(
        "/jobs/run",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.json()["completed"] == ["b", "d"]
    debug = client.get("/_debug/processed").json()["processed"]
    assert debug == ["b", "d"]
