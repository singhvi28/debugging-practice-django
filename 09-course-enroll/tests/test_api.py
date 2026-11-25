import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/courses", {"search": "python"})
    assert res.status_code == 200
    titles = [c["title"] for c in res.json()]
    assert "Intro to Python" in titles


def test_search_partial_match(client):
    res = client.get("/courses", {"search": "data"})
    assert res.status_code == 200
    titles = [c["title"] for c in res.json()]
    assert "Data Structures" in titles


def test_get_missing_course_returns_404(client):
    res = client.get("/courses/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_duplicate_enrollment_returns_409(client):
    res = client.post(
        "/courses/c1/enrollments",
        data=json.dumps({"student_id": "alice"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_enroll_missing_course_returns_404(client):
    res = client.post(
        "/courses/missing/enrollments",
        data=json.dumps({"student_id": "bob"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 404


def test_enroll_student_success(client):
    res = client.post(
        "/courses/c2/enrollments",
        data=json.dumps({"student_id": "carol"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["student_id"] == "carol"


def test_create_course_with_auth(client):
    res = client.post(
        "/courses",
        data=json.dumps({"title": "Algorithms"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
