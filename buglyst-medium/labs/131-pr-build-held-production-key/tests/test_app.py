import json

from deploy import PRODUCTION_SECRET, STAGING_SECRET


def test_fork_pr_to_main_uses_staging_secret(client):
    response = client.post(
        "/deploy/secret",
        data=json.dumps(
            {
                "is_pull_request": True,
                "is_fork": True,
                "target_branch": "main",
            }
        ),
        content_type="application/json",
    )
    body = response.json()
    assert body["secret"] == STAGING_SECRET
    assert body["environment"] == "staging"
    assert body["secret"] != PRODUCTION_SECRET


def test_internal_pr_to_main_still_uses_staging(client):
    response = client.post(
        "/deploy/secret",
        data=json.dumps(
            {
                "is_pull_request": True,
                "is_fork": False,
                "target_branch": "main",
            }
        ),
        content_type="application/json",
    )
    assert response.json()["secret"] == STAGING_SECRET
