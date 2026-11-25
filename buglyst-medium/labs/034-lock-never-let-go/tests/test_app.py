import json


def test_successful_job_releases_lock(client):
    body = {"resource": "inventory-1", "should_fail": False}
    first = client.post(
        "/jobs",
        data=json.dumps(body),
        content_type="application/json",
    )
    second = client.post(
        "/jobs",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert first.status_code == 200
    assert second.status_code == 200


def test_failed_job_releases_lock_for_retry(client):
    resource = "inventory-2"
    failed = client.post(
        "/jobs",
        data=json.dumps({"resource": resource, "should_fail": True}),
        content_type="application/json",
    )
    retry = client.post(
        "/jobs",
        data=json.dumps({"resource": resource, "should_fail": False}),
        content_type="application/json",
    )
    assert failed.status_code == 500
    assert retry.status_code == 200
