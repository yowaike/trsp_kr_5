from app.schemas import TaskStatus


def test_create_task_succeeds(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Подготовить тесты",
            "description": "Написать интеграционные тесты для основных сценариев",
            "status": "todo",
            "priority": 4,
        },
        headers={"X-User-Id": "10"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["owner_id"] == 10


def test_create_task_title_too_short(client):
    response = client.post(
        "/tasks",
        json={"title": "Hi", "status": "todo", "priority": 3},
        headers={"X-User-Id": "10"},
    )

    assert response.status_code == 422


def test_missing_user_header_returns_401(client):
    response = client.post(
        "/tasks",
        json={"title": "Task title", "status": "todo", "priority": 3},
    )

    assert response.status_code == 401


def test_user_sees_only_own_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Task 1", "status": "todo", "priority": 1},
        headers={"X-User-Id": "10"},
    )
    client.post(
        "/tasks",
        json={"title": "Task 2", "status": "done", "priority": 5},
        headers={"X-User-Id": "20"},
    )

    response = client.get("/tasks", headers={"X-User-Id": "10"})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Task 1"


def test_filter_tasks_by_status_and_min_priority(client):
    client.post(
        "/tasks",
        json={"title": "Task 1", "status": "todo", "priority": 2},
        headers={"X-User-Id": "10"},
    )
    client.post(
        "/tasks",
        json={"title": "Task 2", "status": "in_progress", "priority": 4},
        headers={"X-User-Id": "10"},
    )
    client.post(
        "/tasks",
        json={"title": "Task 3", "status": "todo", "priority": 5},
        headers={"X-User-Id": "10"},
    )

    response = client.get(
        "/tasks?status=todo&min_priority=4", headers={"X-User-Id": "10"}
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Task 3"]


def test_update_status_success(client):
    client.post(
        "/tasks",
        json={"title": "Update status", "status": "todo", "priority": 3},
        headers={"X-User-Id": "10"},
    )

    response = client.patch(
        "/tasks/1/status",
        json={"status": "done"},
        headers={"X-User-Id": "10"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_404_for_other_user_task(client):
    client.post(
        "/tasks",
        json={"title": "Private task", "status": "todo", "priority": 2},
        headers={"X-User-Id": "10"},
    )

    response = client.get("/tasks/1", headers={"X-User-Id": "20"})
    assert response.status_code == 404


def test_delete_task_success(client):
    client.post(
        "/tasks",
        json={"title": "Delete me", "status": "todo", "priority": 2},
        headers={"X-User-Id": "10"},
    )

    delete_response = client.delete("/tasks/1", headers={"X-User-Id": "10"})
    assert delete_response.status_code == 204

    get_response = client.get("/tasks/1", headers={"X-User-Id": "10"})
    assert get_response.status_code == 404
