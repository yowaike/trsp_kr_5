def test_users_me_returns_current_user(client):
    response = client.get(
        "/users/me",
        headers={"X-User-Id": "10", "X-User-Role": "user"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 10, "role": "user"}


def test_missing_user_header_401(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_regular_user_forbidden_admin_stats(client):
    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "10", "X-User-Role": "user"},
    )

    assert response.status_code == 403


def test_admin_gets_stats(client):
    client.post(
        "/tasks",
        json={"title": "Stat task", "status": "todo", "priority": 3},
        headers={"X-User-Id": "10"},
    )

    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "1", "X-User-Role": "admin"},
    )

    assert response.status_code == 200
    assert response.json()["total_tasks"] == 1
    assert response.json()["by_status"]["todo"] == 1


def test_regular_user_cannot_delete_other_task(client):
    client.post(
        "/tasks",
        json={"title": "Other task", "status": "todo", "priority": 3},
        headers={"X-User-Id": "10"},
    )

    response = client.delete("/tasks/1", headers={"X-User-Id": "20"})
    assert response.status_code == 404


def test_admin_can_delete_other_task(client):
    client.post(
        "/tasks",
        json={"title": "Admin delete", "status": "todo", "priority": 3},
        headers={"X-User-Id": "10"},
    )

    response = client.delete(
        "/admin/tasks/1",
        headers={"X-User-Id": "2", "X-User-Role": "admin"},
    )

    assert response.status_code == 204
