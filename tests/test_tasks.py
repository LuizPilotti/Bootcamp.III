from fastapi.testclient import TestClient
from src.main import app, reset_database

client = TestClient(app)


def setup_function():
    reset_database()


# --- Cenários Principais (Happy Path) ---

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
    assert data["id"] == 1
    assert data["title"] == "Estudar SDD"
    assert data["completed"] is False


def test_list_tasks():
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_success():
    created = client.post("/tasks", json={"title": "Tarefa Específica"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa Específica"


def test_complete_task():
    created = client.post("/tasks", json={"title": "Tarefa"}).json()
    response = client.patch(f"/tasks/{created['id']}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


# --- Casos de Borda (Edge Cases) ---

def test_list_tasks_empty():
    """Borda: Retorno de lista vazia sem erro"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_missing_title_field():
    """Borda: Payload omitindo o campo title"""
    response = client.post("/tasks", json={"description": "Sem título"})
    assert response.status_code == 422


def test_title_is_required_empty_string():
    """Borda: String vazia"""
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_title_whitespace_only():
    """Borda: String apenas com espaços em branco"""
    response = client.post("/tasks", json={"title": "     "})
    assert response.status_code == 422


def test_get_missing_task():
    """Borda: ID inexistente"""
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_get_task_invalid_id_type():
    """Borda: ID alfanumérico inválido"""
    response = client.get("/tasks/abc")
    assert response.status_code == 422


def test_complete_missing_task():
    """Borda: Concluir tarefa que não existe"""
    response = client.patch("/tasks/999/complete")
    assert response.status_code == 404


def test_complete_task_idempotency():
    """Borda: Concluir tarefa já concluída mantém status 200 e completed=True"""
    created = client.post("/tasks", json={"title": "Tarefa Aberta"}).json()
    client.patch(f"/tasks/{created['id']}/complete")
    response = client.patch(f"/tasks/{created['id']}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_create_task_title_with_surrounding_whitespace():
    """Borda: Título com espaços no início e no fim deve sofrer trim preservando conteúdo"""
    response = client.post(
        "/tasks",
        json={"title": "  Estudar SDD com Test Harness  ", "description": "Iteração 1"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Estudar SDD com Test Harness"


def test_get_task_negative_id_not_found():
    """Borda: ID numérico negativo não existente retorna 404"""
    response = client.get("/tasks/-1")
    assert response.status_code == 404


# --- Novos Cenários de Borda (Ciclo 4 — Testes e Documentação) ---

def test_create_task_default_description():
    """Borda: Quando description é omitido, o valor padrão é string vazia"""
    response = client.post("/tasks", json={"title": "Sem descrição"})
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == ""


def test_create_multiple_tasks_sequential_ids():
    """Borda: IDs devem ser sequenciais e incrementais (1, 2, 3...)"""
    r1 = client.post("/tasks", json={"title": "Tarefa A"})
    r2 = client.post("/tasks", json={"title": "Tarefa B"})
    r3 = client.post("/tasks", json={"title": "Tarefa C"})
    assert r1.json()["id"] == 1
    assert r2.json()["id"] == 2
    assert r3.json()["id"] == 3


def test_complete_task_preserves_title_and_description():
    """Borda: Concluir tarefa não deve alterar título nem descrição"""
    created = client.post(
        "/tasks",
        json={"title": "Minha Tarefa", "description": "Detalhe importante"}
    ).json()
    response = client.patch(f"/tasks/{created['id']}/complete")
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Minha Tarefa"
    assert data["description"] == "Detalhe importante"


def test_health_returns_json_content_type():
    """Borda: Endpoint /health deve retornar Content-Type application/json"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_create_task_with_very_long_title():
    """Borda: Título muito longo deve ser aceito (sem limite superior definido)"""
    long_title = "A" * 1000
    response = client.post("/tasks", json={"title": long_title})
    assert response.status_code == 201
    assert response.json()["title"] == long_title