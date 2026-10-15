from fastapi.testclient import TestClient
from main import app, fake_tasks_db
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    fake_tasks_db.clear()
    yield
    fake_tasks_db.clear()

# 1. Test docs
def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

# 2. Test create
def test_create_task():
    response = client.post("/tasks", json={"title": "Test Task", "priority": 5})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

# 3. Test read all
def test_read_all_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1

# 4. Test read one
def test_read_one_task():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# 5. Test update
def test_update_task():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.put("/tasks/1", json={"title": "Updated Task", "priority": 4})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

# 6. Test delete
def test_delete_task():
    client.post("/tasks", json={"title": "Task 1"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204

# 7. Test missing task (404)
def test_read_missing_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404

# 8. Test validation error (422)
def test_validation_error():
    response = client.post("/tasks", json={"title": "Invalid Task", "priority": 9})
    assert response.status_code == 422