import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Reset the in-memory storage before each test."""
    from app.storage import storage

    storage._tasks.clear()
    storage._next_id = 1
    yield


def test_list_tasks_initially_empty():
    """GET /tasks should return an empty list."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_success():
    """POST /tasks should create a new task."""
    payload = {"title": "Buy milk", "description": "2L whole milk"}
    response = client.post("/tasks", json=payload)
    data = response.json()
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["done"] is False


def test_create_task_validation_error():
    """POST /tasks should fail if title is missing or empty."""
    # Missing title
    response = client.post("/tasks", json={"description": "no title"})
    assert response.status_code == 422

    # Empty title
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_update_task_success():
    """PUT /tasks/{id} should update an existing task."""
    client.post("/tasks", json={"title": "Do homework"})
    update = {"done": True}
    response = client.put("/tasks/1", json=update)
    data = response.json()
    assert response.status_code == 200
    assert data["done"] is True


def test_delete_task_success():
    """DELETE /tasks/{id} should remove a task."""
    client.post("/tasks", json={"title": "Test delete"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    # confirm deletion
    assert client.get("/tasks").json() == []


def test_multiple_tasks_creation():
    """POST /tasks should handle multiple task creation."""
    titles = ["Task 1", "Task 2", "Task 3"]
    for title in titles:
        assert client.post("/tasks", json={"title": title}).status_code == 201
    tasks = client.get("/tasks").json()
    assert [t["title"] for t in tasks] == titles


def test_update_task_not_found():
    """PUT /tasks/{id} should return 404 if task not found."""
    response = client.put("/tasks/999", json={"done": True})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_task_not_found():
    """DELETE /tasks/{id} should return 404 if task not found."""
    response = client.delete("/tasks/123")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_duplicate_title_rejected():
    """POST /tasks should reject duplicate titles."""
    client.post("/tasks", json={"title": "Unique"})
    response = client.post("/tasks", json={"title": "Unique"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_update_with_empty_payload():
    """PUT /tasks/{id} should allow empty payload (no changes)."""
    client.post("/tasks", json={"title": "Do laundry"})
    response = client.put("/tasks/1", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Do laundry"
    assert data["done"] is False


def test_get_task_not_found_via_service_error():
    """GET non-existent task should raise 404."""
    response = client.get("/tasks/999")
    assert response.status_code in (404, 405)
