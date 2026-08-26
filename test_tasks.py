from fastapi.testclient import TestClient
from src.main import app, tasks

client = TestClient(app)


def setup_function():
    tasks.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Estudar SDD", "description": "Fazer os testes"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Estudar SDD"
    assert data["completed"] is False


def test_title_is_required():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_get_missing_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_complete_task():
    created = client.post("/tasks", json={"title": "Tarefa"}).json()
    response = client.patch(f"/tasks/{created['id']}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True
