import json


def test_each_run_gets_its_own_artifact_url(client):
    first = client.post(
        "/artifacts",
        data=json.dumps({"run_id": "run-100", "filename": "bundle.zip"}),
        content_type="application/json",
    ).json()["url"]
    second = client.post(
        "/artifacts",
        data=json.dumps({"run_id": "run-200", "filename": "bundle.zip"}),
        content_type="application/json",
    ).json()["url"]

    assert first == "https://artifacts.example/runs/run-100/bundle.zip"
    assert second == "https://artifacts.example/runs/run-200/bundle.zip"
    assert first != second
