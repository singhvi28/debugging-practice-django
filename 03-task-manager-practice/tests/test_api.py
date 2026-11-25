import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/projects", {"search": "website"})
    assert res.status_code == 200
    names = [p["name"] for p in res.json()]
    assert "Website Redesign" in names


def test_get_missing_project_returns_404(client):
    res = client.get("/projects/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_task_rejects_empty_title(client):
    res = client.post(
        "/projects/p1/tasks",
        data=json.dumps({"title": ""}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400


def test_create_task_persists(client):
    res = client.post(
        "/projects/p1/tasks",
        data=json.dumps({"title": "Write API docs"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    task_id = res.json()["id"]
    tasks = client.get("/projects/p1/tasks").json()
    titles = [t["title"] for t in tasks]
    assert "Write API docs" in titles
    assert any(t["id"] == task_id for t in tasks)


def test_patch_task_works(client):
    res = client.patch(
        "/tasks/t1",
        data=json.dumps({"completed": True}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["completed"] is True


def test_list_projects_without_auth(client):
    res = client.get("/projects")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_create_project_without_auth_is_401(client):
    res = client.post(
        "/projects",
        data=json.dumps({"name": "New Project"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_create_project_with_auth(client):
    res = client.post(
        "/projects",
        data=json.dumps({"name": "API Migration"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "API Migration"
