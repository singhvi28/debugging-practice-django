import os


def test_can_read_vault_file(client):
    res = client.get("/files", {"path": "reports/q1.pdf"})
    assert res.status_code == 200
    assert res.json()["content"] == "Q1 earnings summary"


def test_path_traversal_outside_vault_is_blocked(client):
    secret = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "secret.txt"))
    traversal = "../" + os.path.basename(secret)
    res = client.get("/files", {"path": traversal})
    assert res.status_code == 404


def test_missing_file_returns_404(client):
    res = client.get("/files", {"path": "reports/missing.pdf"})
    assert res.status_code == 404
